from __future__ import annotations

from typing import TYPE_CHECKING, overload

from app_model.types import Action

if TYPE_CHECKING:
    from typing import Any, Callable, Literal, TypeVar

    from app_model import Application, expressions
    from app_model.types import (
        DisposeCallable,
        Icon,  # noqa: F401 ... used in type hints for docs
        IconOrDict,
        KeyBindingRuleOrDict,
        MenuRuleOrDict,
    )

    CommandCallable = TypeVar("CommandCallable", bound=Callable[..., Any])
    CommandDecorator = Callable[[Callable], Callable]


@overload
def register_action(
    app: Application | str, id_or_action: Action
) -> DisposeCallable: ...


@overload
def register_action(
    app: Application | str,
    id_or_action: str,
    title: str,
    *,
    callback: Literal[None] = ...,
    category: str | None = ...,
    tooltip: str | None = ...,
    icon: IconOrDict | None = ...,
    enablement: expressions.Expr | None = ...,
    menus: list[MenuRuleOrDict] | None = ...,
    keybindings: list[KeyBindingRuleOrDict] | None = ...,
    palette: bool = True,
) -> CommandDecorator: ...


@overload
def register_action(
    app: Application | str,
    id_or_action: str,
    title: str,
    *,
    callback: CommandCallable,
    category: str | None = ...,
    tooltip: str | None = ...,
    icon: IconOrDict | None = ...,
    enablement: expressions.Expr | None = ...,
    menus: list[MenuRuleOrDict] | None = ...,
    keybindings: list[KeyBindingRuleOrDict] | None = ...,
    palette: bool = True,
) -> DisposeCallable: ...


def register_action(
    app: Application | str,
    id_or_action: str | Action,
    title: str | None = None,
    *,
    callback: CommandCallable | None = None,
    category: str | None = None,
    tooltip: str | None = None,
    icon: IconOrDict | None = None,
    enablement: expressions.Expr | None = None,
    menus: list[MenuRuleOrDict] | None = None,
    keybindings: list[KeyBindingRuleOrDict] | None = None,
    palette: bool = True,
) -> CommandDecorator | DisposeCallable:
    """Register an action.

    This is a functional form of the
    [`Application.register_action()`][app_model.Application.register_action] method.
    It accepts various overloads to allow for a more concise syntax.  See examples
    below.

    An `Action` is the "complete" representation of a command.  The command is the
    function/callback itself, and an action also includes information about where and
    whether it appears in menus and optional keybinding rules.  Since, most of the
    arguments to this function are simply passed through to the `Action` constructor,
    see also docstrings for:

    - [`Action`][app_model.types.Action]
    - [`CommandRule`][app_model.types.CommandRule]
    - [`MenuRule`][app_model.types.MenuRule]
    - [`KeyBindingRule`][app_model.types.KeyBindingRule]

    Parameters
    ----------
    app: Application | str
        The app in which to register the action. If a string, the app is retrieved
        or created as necessary using
        [`Application.get_or_create(app)`][app_model.Application.get_or_create].
    id_or_action : str | Action
        Either a complete Action object or a string id of the command being registered.
        If an `Action` object is provided, then all other arguments are ignored.
    title : str | None
        Title by which the command is represented in the UI. Required when
        `id_or_action` is a string.
    callback : CommandHandler | None
        Callable object that executes this command, by default None. If not provided,
        a decorator is returned that can be used to decorate a function that executes
        this action.
    category : str | None
        Category string by which the command may be grouped in the UI, by default None
    tooltip : str | None
        Tooltip to show when hovered., by default None
    icon : Icon | None
        [`Icon`][app_model.types.Icon] used to represent this command,
        e.g. on buttons or in menus. by default None
    enablement : expressions.Expr | None
        Condition which must be true to enable the command in in the UI,
        by default None
    menus : list[MenuRuleOrDict] | None
        List of [`MenuRule`][app_model.types.MenuRule] or kwarg `dicts` containing menu
        placements for this action, by default None
    keybindings : list[KeyBindingRuleOrDict] | None
        List of [`KeyBindingRule`][app_model.types.KeyBindingRule] or kwargs `dicts`
        containing default keybindings for this action, by default None
    palette : bool
        Whether to adds this command to the Command Palette, by default True

    Returns
    -------
    CommandDecorator
        If `callback` is not provided, then a decorator is returned that can be used to
        decorate a function as the executor of the command.
    DisposeCallable
        If `callback` is provided, or `id_or_action` is an `Action` object, then a
        function is returned that may be used to unregister the action.

    Raises
    ------
    ValueError
        If `id_or_action` is a string and `title` is not provided.
    TypeError
        If `id_or_action` is not a string or an `Action` object.

    Examples
    --------
    This function can be used directly or as a decorator, and accepts arguments in
    various forms.

    ## Passing an existing Action object

    When the `id_or_action` argument is an instance of `app_model.Action`, then
    all other arguments are ignored, the action object is registered directly, and the
    return value is a function that may be used to unregister the action is returned.

    ```python
    from app_model import Application, Action, register_action

    app = Application.get_or_create("myapp")
    action = Action("my_action", title="My Action", callback=lambda: print("hi"))
    register_action(app, action)

    app.commands.execute_command("my_action")  # prints "hi"
    ```

    ## Creating a new Action

    When the `id_or_action` argument is a string, it is interpreted as the `id`
    of the command being registered, in which case `title` must then also be provided.
    All other arguments are optional, but may be used to customize the action being
    created (with keybindings, menus, icons, etc).

    ```python
    register_action(
        app,
        "my_action2",
        title="My Action2",
        callback=lambda: print("hello again!"),
    )

    app.commands.execute_command("my_action2")  # prints "hello again!"
    ```

    ## Usage as a decorator

    If `callback` is not provided, then a decorator is returned that can be used
    decorate a function as the executor of the command:

    ```python
    @register_action(app, "my_action3", title="My Action3")
    def my_action3():
        print("hello again, again!")


    app.commands.execute_command("my_action3")  # prints "hello again, again!"
    ```

    ## Passing app as a string

    Note that in all of the above examples, the first `app` argument may be either an
    instance of an [`Application`][app_model.Application] object, or a string name of
    an application.  If a string is provided, then the application is retrieved or
    created as necessary using
    [`Application.get_or_create()`][app_model.Application.get_or_create].

    ```python
    register_action(
        "myapp",  # app name instead of Application instance
        "my_action4",
        title="My Action4",
        callback=lambda: print("hello again, again, again!"),
    )
    ```
    """
    if isinstance(id_or_action, Action):
        return _register_action_obj(app, id_or_action)
    if isinstance(id_or_action, str):
        if not title:
            raise ValueError("'title' is required when 'id' is a string")
        return _register_action_str(
            app=app,
            id=id_or_action,
            title=title,
            category=category,
            tooltip=tooltip,
            icon=icon,
            enablement=enablement,
            callback=callback,
            palette=palette,
            menus=menus,
            keybindings=keybindings,
        )
    raise TypeError("'id_or_action' must be a string or an Action")


def _register_action_str(
    app: Application | str, **kwargs: Any
) -> CommandDecorator | DisposeCallable:
    """Create and register an Action with a string id and title.

    Helper for `register_action()`.

    If `kwargs['callback']` is a callable, a complete `Action` is created
    (thereby performing type validation and casting) and registered with the
    corresponding registries. Otherwise a decorator returned that can be used
    to decorate the callable that executes the action.
    """
    if kwargs.get("callback") is not None:
        return _register_action_obj(app, Action(**kwargs))

    def decorator(command: CommandCallable, **k: Any) -> CommandCallable:
        if not callable(command):
            raise TypeError(
                "@register_action decorator must be passed a callable object"
            )
        _register_action_obj(app, Action(**{**kwargs, **k, "callback": command}))
        return command

    decorator.__doc__ = f"Decorate function as callback for command {kwargs['id']!r}"
    return decorator


def _register_action_obj(app: Application | str, action: Action) -> DisposeCallable:
    """Register an Action object. Return a function that unregisters the action.

    Helper for `register_action()`.
    """
    from app_model._app import Application

    app = app if isinstance(app, Application) else Application.get_or_create(app)

    # commands
    disposers = [app.commands.register_action(action)]
    # menus
    if dm := app.menus.append_action_menus(action):
        disposers.append(dm)
    # keybindings
    if dk := app.keybindings.register_action_keybindings(action):
        disposers.append(dk)

    def _dispose() -> None:
        for d in disposers:
            d()

    app._disposers.append((action.id, _dispose))
    return _dispose
