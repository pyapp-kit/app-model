# Overview

`app-model` is a declarative, backend-agnostic schema for a GUI-based application.

The primary goal of this library is to provide a set of types that enable
an application developer to declare the commands, keybindings, macros, etc.
that make up their application.

## Installation

Install from pip

```bash
pip install app-model
```

Or from conda-forge

```bash
conda install -c conda-forge app-model
```

## Usage

See the [Getting Started](getting_started.md) guide for a quick introduction to
`app-model`. See the [API Reference](reference/index.md) for a complete
reference of the types and functions provided by `app-model`.

## Motivation

Why bother with a declarative application model?

1. **It's easier to query the application's state**

    If you want to ask "what commands are available in this application?", or
    "what items are currently in a given menu", you can directly query the
    application registries.  For example, you don't need to find a specific
    `QMenu` instance and iterate its `actions()` to know whether a given item is
    present.

1. **It's easier to modify the application's state**

    For applications that need to be dynamic (e.g. adding and removing menu
    items and actions as plugins are loaded and unloaded), it is convenient to
    have an application model that emits events when modified, with the "view"
    (the actual GUI framework) responding to those events to update the actual
    presentation.

1. **It decouples the structure of the application from the GUI framework**

    This makes it easier to change the GUI framework without having to change the
   application. (Obviously, as an application grows with a particular framework,
   it does become harder to extract, but having a loosely coupled model is a step
   in the right direction)

1. **It's easier to test**

    `app-model` itself is comprehensively tested.  By avoiding a number of
    one-off procedurally created menus, we can test reusable *patterns* of
    command/menu/keybinding creation and registration.

## GUI Frameworks

`app-model` is framework-agnostic, and can be used with any GUI toolkit, but
[Qt](https://www.qt.io) is currently the primary target, and a
[Qt adapter][app_model.backends.qt] comes with this library.

See some details in the [qt section](getting_started.md#qt) of the getting
started guide.

## Example Application

For a working example of a QApplication built with and without `app-model`,
compare
[`demo/model_app.py`](https://github.com/pyapp-kit/app-model/blob/main/demo/model_app.py)
to
[`demo/qapplication.py`](https://github.com/pyapp-kit/app-model/blob/main/demo/qapplication.py)
in the `demo` directory of the `app-model` repository.
