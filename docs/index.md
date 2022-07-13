# Overview

`app-model` is a declarative, backend-agnostic schema for a GUI-based application.

The primary goal of this library is to provide a set of types that enable
an application developer to declare the commands, keybindings, macros, etc.
that make up their application.

## General architecture

Typical usage will begin by creating a [`Application`][app_model.Application]
object. [Commands][app_model.types.CommandRule], [menu items][app_model.types.MenuRule], and [keybindings][app_model.types.KeyBindingRule] will usually be declared by creating
[`Action`][app_model.Action] objects, and  registered with the application
using the [`Application.register_action`][app_model.Application.register_action]

An application maintains a [registry](registries) for all registered [commands][app_model.registries.CommandsRegistry], [menus][app_model.registries.MenusRegistry], and [keybindings][app_model.registries.KeyBindingsRegistry].

!!! Note
    Calling [`Application.register_action`][app_model.Application.register_action] with a single
    [`Action`][app_model.Action] object is just a convenience around independently registering
    objects with each of the registries using:

    - [CommandsRegistry.register_command][app_model.registries.CommandsRegistry.register_command]
    - [MenusRegistry.append_menu_items][app_model.registries.MenusRegistry.append_menu_items]
    - [KeyBindingsRegistry.register_keybinding_rule][app_model.registries.KeyBindingsRegistry.register_keybinding_rule]

## Motivation

Why bother with a declarative application model?

1. **It's easier to query the application's state**

    If you want to ask "what commands are available in this application?", or "what items are currently in a given menu", you can directly query the application registries.  For example, you don't need to find a specific `QMenu` instance and iterate it's `actions()` to know whether a given item is present.

1. **It's easier to modify the application's state**

    For applications that need to be dynamic (e.g. adding and removing menu items and actions as plugins are loaded and unloaded), it is convenient to have an application
    model that emits events when modified, with the "view" (the actual GUI backend) responding to those events to update the actual presentation.

1. **It decouples the structure of the application from the underlying backend**

    This makes it it easier to change the backend without having to change the
   application. (Obviously, as an application grows with a particular backend,
   it does become harder to extract, but having a losely coupled model is a step
   in the right direction)

1. **It's easier to test**

    `app-model` itself is comprehensively tested.  By avoiding a number of
    one-off procedurally created menus, we can test reusable *patterns* of
    command/menu/keybinding creation and registration.

## Back Ends

`app-model` is backend-agnostic, and can be used with any GUI toolkit, but [Qt](https://www.qt.io) is
currently the primary target, and a Qt-backend comes with this library.

### Qt backend

Once objects have been registered with the application, it becomes very easy to create
Qt objects (such as [`QMainWindow`](https://doc.qt.io/qt-6/qmainwindow.html), [`QMenu`](https://doc.qt.io/qt-6/qmenu.html), [`QMenuBar`](https://doc.qt.io/qt-6/qmenubar.html), [`QAction`](https://doc.qt.io/qt-6/qaction.html), [`QToolBar`](https://doc.qt.io/qt-6/qtoolbar.html), etc...) with very minimal boilerplate and repetitive procedural code.

```python
from app_model import Application, Action
from app_model.backends.qt import QModelMenu

app = Application("my-app")
action = Action(id="my-action", ..., menus=[{'id': 'file', ...}])
app.register_action(action)

qmenu = QModelMenu(menu_id='file', app=app)
```

!!! Tip
    Application [registries](registries) are backed by
    [psygnal](https://github.com/tlambert03/psygnal), and emit events when
    modified.  These events are connected to the Qt objects, so `QModel...`
    objects such as `QModelMenu` and `QCommandAction` will be updated when the
    application's registry is updated.

### Example Application

For a working example of a QApplication built with and without `app-model`, compare [`demo/model_app.py`](https://github.com/napari/app-model/blob/main/demo/model_app.py) to [`demo/qapplication.py`](https://github.com/napari/app-model/blob/main/demo/qapplication.py) in the `demo` directory of the `app-model` repository.
