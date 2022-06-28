from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
from typing import TYPE_CHECKING, Any, Callable, Optional

from psygnal import Signal

from ._types import MenuItem, SubmenuItem, _RegisteredCommand, _RegisteredKeyBinding

if TYPE_CHECKING:
    from typing import Dict, Iterator, List, Sequence, Set, Tuple, Union

    from ._types import CommandCallable, CommandIdStr, KeybindingRule

    DisposeCallable = Callable[[], None]
    CommandDecorator = Callable[[CommandCallable], CommandCallable]
    MenuOrSubmenu = Union[MenuItem, SubmenuItem]


class CommandsRegistry:

    registered = Signal(str)
    __instance: Optional[CommandsRegistry] = None

    def __init__(self) -> None:
        self._commands: Dict[CommandIdStr, List[_RegisteredCommand]] = {}

    @classmethod
    def instance(cls) -> CommandsRegistry:
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def register_command(
        self,
        id: CommandIdStr,
        callback: CommandCallable,
        title: str = "",
    ) -> DisposeCallable:
        """Register a callable as the handler for command `id`.

        Parameters
        ----------
        id : CommandId
            Command identifier
        callback : Callable
            Callable to be called when the command is executed
        title : str
            Optional title for the command.

        Returns
        -------
        DisposeCallable
            A function that can be called to unregister the command.
        """
        commands = self._commands.setdefault(id, [])

        cmd = _RegisteredCommand(id, callback, title)
        commands.insert(0, cmd)

        def _dispose() -> None:
            commands.remove(cmd)
            if not commands:
                del self._commands[id]

        self.registered.emit(id)
        return _dispose

    def __iter__(self) -> Iterator[Tuple[CommandIdStr, List[_RegisteredCommand]]]:
        yield from self._commands.items()

    def __contains__(self, id: str) -> bool:
        return id in self._commands

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"<{name} at {hex(id(self))} ({len(self._commands)} commands)>"

    def __getitem__(self, id: CommandIdStr) -> List[_RegisteredCommand]:
        """Retrieve commands registered under a given ID"""
        return self._commands[id]

    def execute_command(
        self,
        id: CommandIdStr,
        *args: Any,
        execute_asychronously: bool = False,
        **kwargs: Any,
    ) -> Future:
        """Execute a registered command

        Parameters
        ----------
        id : CommandId
            ID of the command to execute
        execute_asychronously : bool
            Whether to execute the command asynchronously in a thread,
            by default `False`.  Note that *regardless* of this setting,
            the return value will implement the `Future` API (so it's necessary)
            to call `result()` on the returned object.  Eventually, this will
            default to True, but we need to solve `ensure_main_thread` Qt threading
            issues first

        Returns
        -------
        Future: conconrent.futures.Future
            Future object containing the result of the command

        Raises
        ------
        KeyError
            If the command is not registered or has no callbacks.
        """
        if cmds := self[id]:
            # TODO: decide whether we'll ever have more than one command
            # and if so, how to handle it
            cmd = cmds[0].run_injected
        else:
            raise KeyError(f'Command "{id}" has no registered callbacks')

        if execute_asychronously:
            with ThreadPoolExecutor() as executor:
                return executor.submit(cmd, *args, **kwargs)
        else:
            future: Future = Future()
            try:
                future.set_result(cmd(*args, **kwargs))
            except Exception as e:
                future.set_exception(e)
            return future

    def __str__(self) -> str:
        lines: list = []
        for id, cmds in self:
            lines.extend(f"{id!r:<32} -> {cmd.title!r}" for cmd in cmds)
        return "\n".join(lines)


class KeybindingsRegistry:

    registered = Signal()
    __instance: Optional[KeybindingsRegistry] = None

    def __init__(self) -> None:
        self._coreKeybindings: List[_RegisteredKeyBinding] = []

    @classmethod
    def instance(cls) -> KeybindingsRegistry:
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def register_keybinding_rule(
        self, id: CommandIdStr, rule: KeybindingRule
    ) -> Optional[DisposeCallable]:
        if bound_keybinding := rule._bind_to_current_platform():
            entry = _RegisteredKeyBinding(
                keybinding=bound_keybinding,
                command_id=id,
                weight=rule.weight,
                when=rule.when,
            )
            self._coreKeybindings.append(entry)
            self.registered.emit()

            def _dispose() -> None:
                self._coreKeybindings.remove(entry)

            return _dispose
        return None  # pragma: no cover

    def __iter__(self) -> Iterator[_RegisteredKeyBinding]:
        yield from self._coreKeybindings

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"<{name} at {hex(id(self))} ({len(self._coreKeybindings)} bindings)>"


class MenuRegistry:
    menus_changed = Signal(set)
    __instance: Optional[MenuRegistry] = None

    def __init__(self) -> None:
        self._menu_items: Dict[str, List[MenuOrSubmenu]] = {}

    @classmethod
    def instance(cls) -> MenuRegistry:
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def append_menu_items(
        self, items: Sequence[Tuple[str, MenuOrSubmenu]]
    ) -> DisposeCallable:
        changed_ids: Set[str] = set()
        disposers: List[Callable[[], None]] = []

        for id, item in items:
            menu_list = self._menu_items.setdefault(id, [])
            menu_list.append(item)
            changed_ids.add(id)
            disposers.append(lambda: menu_list.remove(item))

        def _dispose() -> None:
            for disposer in disposers:
                disposer()
            for id in changed_ids:
                if not self._menu_items.get(id):
                    del self._menu_items[id]
            self.menus_changed.emit(changed_ids)

        if changed_ids:
            self.menus_changed.emit(changed_ids)

        return _dispose

    def __iter__(
        self,
    ) -> Iterator[Tuple[str, List[MenuOrSubmenu]]]:
        yield from self._menu_items.items()

    def __contains__(self, id: object) -> bool:
        return id in self._menu_items

    def get_menu(self, menu_id: str) -> List[MenuOrSubmenu]:
        return self._menu_items[menu_id]

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"<{name} at {hex(id(self))} ({len(self._menu_items)} menus)>"

    def __str__(self) -> str:
        return "\n".join(self._render())

    def _render(self) -> List[str]:
        """Return registered menu items as lines of strings."""
        lines = []

        branch = "  ├──"
        for menu in self._menu_items:
            lines.append(menu)
            for group in self.iter_menu_groups(menu):
                first = next(iter(group))
                lines.append(f"  ├───────────{first.group}───────────────")
                for child in group:
                    if isinstance(child, MenuItem):
                        lines.append(
                            f"{branch} {child.command.title} ({child.command.id})"
                        )
                    else:
                        lines.extend(
                            [
                                f"{branch} {child.submenu}",
                                "  ├──  └── ...",
                            ]
                        )
            lines.append("")
        return lines

    def iter_menu_groups(self, menu_id: str) -> Iterator[List[MenuOrSubmenu]]:
        yield from MenuRegistry._sorted_groups(self.get_menu(menu_id))

    @staticmethod
    def _sorted_groups(
        items: List[MenuOrSubmenu],
        group_sorter: Callable = lambda x: 0 if x == "navigation" else 1,
        order_sorter: Callable = lambda x: getattr(x, "order", "") or 0,
    ) -> Iterator[List[MenuOrSubmenu]]:
        """Sort a list of menu items based on their .group and .order attributes."""
        groups: dict[Optional[str], List[MenuOrSubmenu]] = {}
        for item in items:
            groups.setdefault(item.group, []).append(item)

        for group_id in sorted(groups, key=group_sorter):
            yield sorted(groups[group_id], key=order_sorter)
