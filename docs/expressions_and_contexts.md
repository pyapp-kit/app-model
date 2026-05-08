# Expressions and Contexts

`app-model` provides two complementary primitives that let you describe
*conditional behavior* in your application without having to evaluate that
condition immediately:

- **Expressions** ([`Expr`][app_model.expressions.Expr]) are abstract,
  serializable representations of conditional statements (e.g. `"x > 5 and
  is_ready"`).  They have *no value* on their own — they need to be evaluated
  against some context.
- **Contexts** ([`Context`][app_model.expressions.Context]) are mappings of
  names to concrete values (e.g. `{"x": 7, "is_ready": True}`).  They provide
  the values that an expression needs in order to be evaluated.

This separation makes it possible to *declare* a condition (in code, in a
plugin manifest, in a config file...) and *evaluate* it later, against a state
that may change over time.

A common use is to control whether a menu item is visible or a keybinding is
active.  An [`Action`][app_model.Action] may, for example, declare that it is
only enabled when `selected_layer_count > 0`.  The application is then
responsible for keeping the relevant context keys up to date, and the menu/
keybinding system will re-evaluate the expression as the context changes.

## A motivating example

Standard Python expressions like `x > 5 and y == 'hello'` are evaluated
immediately and reduce to a single value.  To delay evaluation, you might
keep them as strings and evaluate later with `eval`:

```python
expression = "x > 5 and y == 'hello'"

eval(expression, {"x": 7, "y": "hello"})  # True
eval(expression, {"x": 1, "y": "hello"})  # False
```

This works, but `eval` is unsafe (it executes arbitrary Python), and a plain
string isn't very ergonomic to construct, combine, or introspect.
`app-model` provides a richer abstraction for this kind of deferred
conditional logic.

## Expressions

[`Expr`][app_model.expressions.Expr] is the abstract base class for an
expression.  An `Expr` is an `ast.AST` subclass — it represents a parsed
expression tree, but does not yet have a value.  You typically don't
instantiate `Expr` directly; instead, you parse a string with
[`parse_expression`][app_model.expressions.parse_expression]:

```python
from app_model.expressions import parse_expression

expr = parse_expression("x > 5 and y == 'hello'")

expr.eval({"x": 7, "y": "hello"})  # True
expr.eval({"x": 1, "y": "hello"})  # False
```

For convenience, [`safe_eval`][app_model.expressions.safe_eval] parses and
evaluates in one step:

```python
from app_model.expressions import safe_eval

safe_eval("x > 5 and y == 'hello'", {"x": 7, "y": "hello"})  # True
```

### What's supported (and what's not)

Unlike `eval`, parsing an `Expr` only allows a safe subset of Python.
Supported constructs include:

- **Names**: `myvar` (require a context to evaluate)
- **Constants**: numbers, strings, bytes, booleans, `None`
- **Comparisons**: `==`, `!=`, `<`, `<=`, `>`, `>=`, `in`, `not in`
- **Boolean operators**: `and`, `or`, `not`
- **Binary operators**: `+`, `-`, `*`, `/`, `//`, `%`, `**`, `@`, `^`,
  `&`, `|`
- **Unary operators**: `not`, `-`, `+`, `~`
- **Conditional expressions**: `a if b else c`
- **Container literals**: lists, tuples, sets (e.g. `x in [1, 2, 3]`)

The following are explicitly *not* supported (and will raise `SyntaxError`):

- attribute access (`obj.attr`)
- function calls (`f(x)`)
- indexing or slicing (`x[0]`, `x[1:2]`)
- f-strings
- the walrus operator (`a := 1`)
- comprehensions
- statements & assignments

### Building expressions in code

You can also build expressions directly from
[`Name`][app_model.expressions.Name] and
[`Constant`][app_model.expressions.Constant] nodes, using normal Python
operators.  This is convenient when you want to construct expressions
programmatically (and gives nice IDE autocompletion when combined with
`ContextKey`, see below):

```python
from app_model.expressions import Name, Constant

light_is_green = Name[bool]("light_is_green")
count = Name[int]("count")

is_ready = light_is_green & (count > 5)

is_ready.eval({"count": 4, "light_is_green": True})  # False
is_ready.eval({"count": 7, "light_is_green": False}) # False
is_ready.eval({"count": 7, "light_is_green": True})  # True
```

!!! note "About `&`, `|`, and `~`"

    When working with `Expr` objects, the bitwise operators `&`, `|`, and
    `~` are overloaded to mean boolean `and`, `or`, and `not`.

    This is necessary because Python's `and`/`or`/`not` keywords cannot be
    overloaded — using them on `Expr` objects would short-circuit and just
    return one of the operands, instead of building a new expression.

    If you actually need bitwise operations, use the
    [`bitand`][app_model.expressions.Expr.bitand] and
    [`bitor`][app_model.expressions.Expr.bitor] methods.

Expressions can be serialized back to strings (e.g. for storage or display):

```python
str(is_ready)
# 'light_is_green and count > 5'
```

## Contexts

A [`Context`][app_model.expressions.Context] is a mapping of names to values
that can be used to evaluate an expression.  For simple cases, a plain `dict`
will do — but the `Context` class adds two important capabilities:

1. It is a [`ChainMap`][collections.ChainMap], so contexts can have
   parents and children (created with
   [`new_child`][app_model.expressions.Context.new_child]).  Children inherit keys
   from their parents, but can add or override keys locally.
2. It is **evented**: the
   [`changed`][app_model.expressions.Context.changed] signal is emitted
   whenever a key is added, modified, or deleted.  Child contexts re-emit
   their parent's events, so anything listening to a child sees changes
   from anywhere in the chain.

```python
from app_model.expressions import Context

root = Context()
root["theme"] = "dark"

scoped = root.new_child()
scoped["selected_count"] = 3

# child sees keys from parent
scoped["theme"]           # 'dark'
scoped["selected_count"]  # 3

@scoped.changed.connect
def on_change(keys):
    print("changed:", keys)

root["theme"] = "light"   # changed: {'theme'}
scoped["selected_count"] = 7  # changed: {'selected_count'}
```

When you need to make several changes at once and only emit a single event,
use [`buffered_changes`][app_model.expressions.Context.buffered_changes]:

```python
with scoped.buffered_changes():
    scoped["a"] = 1
    scoped["b"] = 2
# only one `changed` event is emitted, with keys={'a', 'b'}
```

### Creating contexts for objects

A typical pattern is to associate a context with an object — for example, a
window, a document, or a viewer.  When operations happen *inside* that
object (or inside a child object created by it), they should see that
object's context.

You *could* just instantiate a `Context()` and stash it on the object
yourself:

```python
class Window:
    def __init__(self):
        self.context = Context()           # an isolated root mapping
        self.document = Document()         # has no idea about Window's context
```

…but this gives you an isolated, parentless mapping that nothing else can
discover. If `Document` (or anything created inside `Window.__init__`)
wants the same context, you have to thread it through manually.

[`create_context`][app_model.expressions.create_context] does three extra
things on top of `Context()` to solve this:

1. **It registers the context** in a process-wide table keyed by
   `id(obj)`, so any code can retrieve it later via
   [`get_context(obj)`][app_model.expressions.get_context] — no need to
   hold or pass a reference.
2. **It cleans up the registry entry** when `obj` is garbage-collected,
   via `weakref.finalize`, so the table doesn't leak.
3. **It auto-discovers a parent** by walking up the call stack looking
   for a `self` in some enclosing frame that already has a registered
   context. The new context is then created as a `ChainMap` child of
   that parent (falling back to a process-wide root if none is found).

That last point is the magic that makes nested objects automatically share
context without explicit wiring:

```python
from app_model.expressions import create_context, get_context

class Window:
    def __init__(self):
        create_context(self)
        self.document = Document()        # constructed inside Window.__init__

class Document:
    def __init__(self):
        create_context(self)              # picks Window's context as parent

w = Window()
get_context(w)              # Window's context
get_context(w.document)     # Document's context (a ChainMap child of Window's)

get_context(w)["theme"] = "dark"
get_context(w.document)["theme"]   # 'dark' — inherited from Window
```

If `Document` had used `Context()` directly, `get_context(w.document)` would
return `None`, the `Document`'s context would be a sibling root rather than
a child, and `theme` would not be visible from inside the document.

### Application contexts

The [`Application`][app_model.Application] class automatically creates a
[`Context`][app_model.expressions.Context] for itself, available as
`app.context`.  It is pre-populated with a few platform-detection keys via
[`app_model_context`][app_model.expressions.app_model_context]:

| Key | Type | Meaning |
| --- | ---- | ------- |
| `is_linux` | `bool` | Running on Linux |
| `is_mac` | `bool` | Running on macOS |
| `is_windows` | `bool` | Running on Windows |

Anything you put in `app.context` is available to expressions used in
[`Action`][app_model.Action] enablement rules, menu `when` clauses, and
keybinding `when` clauses.

## Context keys: typed, documented names

Strings like `"selected_count"` are easy to typo and hard to discover.
[`ContextKey`][app_model.expressions.ContextKey] is a named, documented,
optionally-typed expression node.  It subclasses
[`Name`][app_model.expressions.Name], so a `ContextKey` *is* an expression
that you can compose with other expressions using normal operators.

`ContextKey`s are organized into
[`ContextNamespace`][app_model.expressions.ContextNamespace] subclasses:

```python
from app_model.expressions import ContextKey, ContextNamespace

class SelectionContextKeys(ContextNamespace[list]):
    selected_count = ContextKey(
        default_value=0,
        description="Number of currently selected items.",
        getter=lambda selection: len(selection),
    )
    has_selection = ContextKey(
        default_value=False,
        description="Whether anything is selected.",
        getter=lambda selection: len(selection) > 0,
    )
```

Each `ContextKey` has:

- a **default value** (used when the key isn't in the context yet)
- a **description** (useful for documentation)
- an optional **getter** — a function that, given some source object, returns
  the current value for that key

Because `ContextKey` is itself an expression, you can compose it directly:

```python
expr = SelectionContextKeys.selected_count > 0
expr.eval({"selected_count": 3})  # True
expr.eval({"selected_count": 0})  # False
```

This is much friendlier to write and refactor than `parse_expression(
"selected_count > 0")`, and gives you static type information for free.

### Binding a namespace to a context

Once instantiated, a `ContextNamespace` is bound to a particular
`Context`.  Its declared keys then act as live get/set descriptors on that
context, with the right defaults applied:

```python
from app_model.expressions import Context

ctx = Context()
keys = SelectionContextKeys(ctx)

keys.selected_count          # 0 (default)
ctx["selected_count"]        # 0

keys.selected_count = 3      # sets ctx["selected_count"] = 3
ctx["selected_count"]        # 3

keys.dict()
# {'selected_count': 3, 'has_selection': False}

keys.reset_all()             # restore defaults
```

This gives you a typed, attribute-style API on top of a plain mapping —
useful for keeping context updates close to the model objects that drive
them.

### Discovering all declared keys

Every `ContextKey` you declare is recorded in a process-wide registry,
which is convenient for documentation generation:

```python
from app_model.expressions import ContextKey

for info in ContextKey.info():
    print(info.key, info.type, info.description)
```

Each entry is a [`ContextKeyInfo`][app_model.expressions.ContextKeyInfo]
named tuple with `key`, `type`, `description`, and `namespace` fields.

## Putting it all together

Several `app-model` types accept `Expr` instances as conditions:

- [`CommandRule.enablement`][app_model.types.CommandRule] — when a command is
  enabled in the UI
- [`MenuRule.when`][app_model.types.MenuRule] — when a menu item is shown
- [`KeyBindingRule.when`][app_model.types.KeyBindingRule] — when a keybinding
  is active
- [`ToggleRule.condition`][app_model.types.ToggleRule] — when a command
  should appear "checked" in the UI

A typical end-to-end pattern looks like:

```python
from app_model import Action, Application
from app_model.expressions import ContextKey, ContextNamespace
from app_model.types import KeyBindingRule, KeyCode, KeyMod

class MyKeys(ContextNamespace[list]):
    selected_count = ContextKey(
        default_value=0,
        description="Number of selected items",
        getter=lambda sel: len(sel),
    )

app = Application("my-app")
keys = MyKeys(app.context)

def delete_selection():
    print("deleted!")

app.register_action(
    Action(
        id="delete",
        title="Delete",
        callback=delete_selection,
        enablement=MyKeys.selected_count > 0,
        keybindings=[
            KeyBindingRule(
                primary=KeyMod.CtrlCmd | KeyCode.Delete,
                when=MyKeys.selected_count > 0,
            )
        ],
    )
)

# Later, as your application's selection state changes, update the context.
# Anything looking at the action's `enablement` (e.g. a Qt menu) will be
# notified via the Context's `changed` signal and can refresh its state.
keys.selected_count = 0  # action becomes disabled
keys.selected_count = 2  # action becomes enabled
```

### Summary

1. Define the names you care about with `ContextKey` inside a
   `ContextNamespace`.
2. Use those keys to build `Expr` objects that describe the conditions
   under which actions, menus, and keybindings should be enabled or shown.
3. Maintain a `Context` that holds the current values for those keys, and
   keep it in sync with your application state.
4. The `changed` signal on the context will let any consumers (menus,
   keybindings, etc.) re-evaluate the relevant expressions whenever
   anything they depend on changes.
