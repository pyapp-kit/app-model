from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, overload

from ..types import Action, MenuItem

if TYPE_CHECKING:
    from typing import Any, Callable, List, Literal, Optional, Union

    from .. import expressions
    from .._app import Application
    from ..types import IconOrDict, KeyBindingRuleOrDict, MenuRuleOrDict
    from ..types._constants import DisposeCallable

    CommandCallable = TypeVar("CommandCallable", bound=Callable[..., Any])
    CommandDecorator = Callable[[Callable], Callable]


@overload
def register_action(
    app: Union[Application, str], id_or_action: Action
) -> DisposeCallable:
    ...


@overload
def register_action(
    app: Union[Application, str],
    id_or_action: str,
    title: str,
    *,
    callback: Literal[None] = None,
    category: Optional[str] = None,
    tooltip: Optional[str] = None,
    icon: Optional[IconOrDict] = None,
    enablement: Optional[expressions.Expr] = None,
    menus: Optional[List[MenuRuleOrDict]] = None,
    keybindings: Optional[List[KeyBindingRuleOrDict]] = None,
    add_to_command_palette: bool = True,
) -> CommandDecorator:
    ...


@overload
def register_action(
    app: Union[Application, str],
    id_or_action: str,
    title: str,
    *,
    callback: CommandCallable,
    category: Optional[str] = None,
    tooltip: Optional[str] = None,
    icon: Optional[IconOrDict] = None,
    enablement: Optional[expressions.Expr] = None,
    menus: Optional[List[MenuRuleOrDict]] = None,
    keybindings: Optional[List[KeyBindingRuleOrDict]] = None,
    add_to_command_palette: bool = True,
) -> DisposeCallable:
    ...


def register_action(
    app: Union[Application, str],
    id_or_action: Union[str, Action],
    title: Optional[str] = None,
    *,
    callback: Optional[CommandCallable] = None,
    category: Optional[str] = None,
    tooltip: Optional[str] = None,
    icon: Optional[IconOrDict] = None,
    enablement: Optional[expressions.Expr] = None,
    menus: Optional[List[MenuRuleOrDict]] = None,
    keybindings: Optional[List[KeyBindingRuleOrDict]] = None,
    add_to_command_palette: bool = True,
) -> Union[CommandDecorator, DisposeCallable]:
    """Register an action.

    An Action is the "complete" representation of a command.  The command is the
    function itself, and an action also includes information about where and whether
    it appears in menus and optional keybinding rules.

    see also docstrings for:

    - :class:`~app_model._types.Action`
    - :class:`~app_model._types.CommandRule`
    - :class:`~app_model._types.MenuRule`
    - :class:`~app_model._types.KeyBindingRule`

    This function can be used directly or as a decorator:

    - When the first `id_or_action` argument is an `Action`, then all other arguments
      are ignored, the action object is registered directly, and a function that may be
      used to unregister the action is returned.
    - When the first `id_or_action` argument is a string, it is interpreted as the `id`
      of the command being registered, and `title` must then also be provided. If `run`
      is not provided, then a decorator is returned that can be used to decorate the
      callable that executes the command; otherwise the command is registered directly
      and a function that may be used to unregister the action is returned.

    Parameters
    ----------
    app: Union[Application, str]
        The app in which to register the action. If a string, the app is retrieved
        or created as necessary using `Application.get_or_create(app)`.
    id_or_action : Union[CommandId, Action]
        Either a complete Action object or a string id of the command being registered.
        If an `Action` object is provided, then all other arguments are ignored.
    title : Optional[str]
        Title by which the command is represented in the UI. Required when
        `id_or_action` is a string.
    callback : Optional[CommandHandler]
        Callable object that executes this command, by default None. If not provided,
        a decorator is returned that can be used to decorate a function that executes
        this action.
    category : Optional[str]
        Category string by which the command may be grouped in the UI, by default None
    tooltip : Optional[str]
        Tooltip to show when hovered., by default None
    icon : Optional[Icon]
        :class:`~app_model._types.Icon` used to represent this command,
        e.g. on buttons or in menus. by default None
    enablement : Optional[context.Expr]
        Condition which must be true to enable the command in in the UI,
        by default None
    menus : Optional[List[MenuRuleOrDict]]
        :class:`~app_model._types.MenuRule` or `dicts` containing menu
        placements for this action, by default None
    keybindings : Optional[List[KeyBindingRuleOrDict]]
        :class:`~app_model._types.KeyBindingRule` or `dicts` containing
        default keybindings for this action, by default None
    add_to_command_palette : bool
        Whether to adds this command to the Command Palette, by default True

    Returns
    -------
    Union[CommandDecorator, DisposeCallable]
        If `run` is not provided, then a decorator is returned.
        If `run` is provided, or `id_or_action` is an `Action` object, then a function
        that may be used to unregister the action is returned.

    Raises
    ------
    ValueError
        If `id_or_action` is a string and `title` is not provided.
    TypeError
        If `id_or_action` is not a string or an `Action` object.
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
            add_to_command_palette=add_to_command_palette,
            menus=menus,
            keybindings=keybindings,
        )
    raise TypeError("'id_or_action' must be a string or an Action")


def _register_action_str(
    app: Union[Application, str],
    **kwargs: Any,
) -> Union[CommandDecorator, DisposeCallable]:
    """Create and register an Action with a string id and title.

    Helper for `register_action()`.

    If `kwargs['run']` is a callable, a complete `Action` is created
    (thereby performing type validation and casting) and registered with the
    corresponding registries. Otherwise a decorator returned that can be used
    to decorate the callable that executes the action.
    """
    if callable(kwargs.get("callback")):
        return _register_action_obj(app, Action(**kwargs))

    def decorator(command: CommandCallable, **k: Any) -> CommandCallable:
        _register_action_obj(app, Action(**{**kwargs, **k, "callback": command}))
        return command

    decorator.__doc__ = f"Decorate function as callback for command {kwargs['id']!r}"
    return decorator


def _register_action_obj(
    app: Union[Application, str],
    action: Action,
) -> DisposeCallable:
    """Register an Action object. Return a function that unregisters the action.

    Helper for `register_action()`.
    """
    from .._app import Application

    app = app if isinstance(app, Application) else Application.get_or_create(app)

    # command
    disp_cmd = app.commands.register_command(action.id, action.callback, action.title)
    disposers = [disp_cmd]

    # menu
    items = []
    for rule in action.menus or ():
        menu_item = MenuItem(
            command=action, when=rule.when, group=rule.group, order=rule.order
        )
        items.append((rule.id, menu_item))
    disposers.append(app.menus.append_menu_items(items))

    if action.add_to_command_palette:
        menu_item = MenuItem(command=action, when=action.enablement)
        disp = app.menus.append_menu_items([(app.menus.COMMAND_PALETTE_ID, menu_item)])
        disposers.append(disp)

    # keybinding
    for keyb in action.keybindings or ():
        if action.enablement is not None:
            _keyb = keyb.copy()
            if _keyb.when is None:
                _keyb.when = action.enablement
            else:
                _keyb.when = action.enablement | _keyb.when
        else:
            _keyb = keyb
        if _d := app.keybindings.register_keybinding_rule(action.id, _keyb):
            disposers.append(_d)

    def _dispose() -> None:
        for d in disposers:
            d()

    app._disposers.append((action.id, _dispose))
    return _dispose
