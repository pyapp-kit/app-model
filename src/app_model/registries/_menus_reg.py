from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Final, Iterable, Iterator

from psygnal import Signal

from app_model.types import MenuItem

if TYPE_CHECKING:
    from app_model.types import Action, DisposeCallable, MenuOrSubmenu

MenuId = str


class MenusRegistry:
    """Registry for menu and submenu items."""

    COMMAND_PALETTE_ID: Final = "_command_pallet_"
    menus_changed = Signal(set)

    def __init__(self) -> None:
        self._menu_items: dict[MenuId, dict[MenuOrSubmenu, None]] = {}

    def append_action_menus(self, action: Action) -> DisposeCallable | None:
        """Append all MenuRule items declared in `action.menus`.

        Parameters
        ----------
        action : Action
            The action containing menus to append.

        Returns
        -------
        DisposeCallable | None
            A function that can be called to unregister the menu items. If no
            menu items were registered, returns `None`.
        """
        disposers: list[Callable[[], None]] = []
        disp1 = self.append_menu_items(
            (
                rule.id,
                MenuItem(
                    command=action, when=rule.when, group=rule.group, order=rule.order
                ),
            )
            for rule in action.menus or ()
        )
        disposers.append(disp1)

        if action.palette:
            menu_item = MenuItem(command=action, when=action.enablement)
            disp = self.append_menu_items([(self.COMMAND_PALETTE_ID, menu_item)])
            disposers.append(disp)

        if not disposers:  # pragma: no cover
            return None

        def _dispose() -> None:
            for disposer in disposers:
                disposer()

        return _dispose

    def append_menu_items(
        self, items: Iterable[tuple[MenuId, MenuOrSubmenu]]
    ) -> DisposeCallable:
        """Append menu items to the registry.

        Parameters
        ----------
        items : Iterable[Tuple[str, MenuOrSubmenu]]
            Items to append.

        Returns
        -------
        DisposeCallable
            A function that can be called to unregister the menu items.
        """
        changed_ids: set[str] = set()
        disposers: list[Callable[[], None]] = []
        for menu_id, item in items:
            item = MenuItem._validate(item)  # type: ignore
            menu_dict = self._menu_items.setdefault(menu_id, {})
            menu_dict[item] = None
            changed_ids.add(menu_id)

            def _remove(dct: dict = menu_dict, _item: Any = item) -> None:
                dct.pop(_item, None)

            disposers.append(_remove)

        def _dispose() -> None:
            for disposer in disposers:
                disposer()
            for id_ in changed_ids:
                if not self._menu_items.get(id_):
                    del self._menu_items[id_]
            self.menus_changed.emit(changed_ids)

        if changed_ids:
            self.menus_changed.emit(changed_ids)

        return _dispose

    def __iter__(
        self,
    ) -> Iterator[tuple[MenuId, Iterable[MenuOrSubmenu]]]:
        yield from self._menu_items.items()

    def __contains__(self, id: object) -> bool:
        return id in self._menu_items

    def get_menu(self, menu_id: MenuId) -> list[MenuOrSubmenu]:
        """Return menu items for `menu_id`."""
        # using method rather than __getitem__ so that subclasses can use arguments
        return list(self._menu_items[menu_id])

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"<{name} at {hex(id(self))} ({len(self._menu_items)} menus)>"

    def __str__(self) -> str:
        return "\n".join(self._render())

    def _render(self) -> list[str]:
        """Return registered menu items as lines of strings."""
        # this is mostly here as a debugging tool.  Can be removed or improved later.
        lines: list[str] = []

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

    def iter_menu_groups(self, menu_id: MenuId) -> Iterator[list[MenuOrSubmenu]]:
        """Iterate over menu groups for `menu_id`.

        Groups are broken into sections (lists of menu or submenu items) based on
        their `group` attribute.  And each group is sorted by `order` attribute.

        Parameters
        ----------
        menu_id : str
            The menu ID to return groups for.

        Yields
        ------
        Iterator[List[MenuOrSubmenu]]
            Iterator of menu/submenu groups.
        """
        if menu_id in self:
            yield from _sort_groups(self.get_menu(menu_id))


def _sort_groups(
    items: list[MenuOrSubmenu],
    group_key: Callable = lambda x: "0000" if x == "navigation" else x or "",
    order_key: Callable = lambda x: getattr(x, "order", "") or 0,
) -> Iterator[list[MenuOrSubmenu]]:
    """Sort a list of menu items based on their .group and .order attributes."""
    groups: dict[str | None, list[MenuOrSubmenu]] = {}
    for item in items:
        groups.setdefault(item.group, []).append(item)

    for group_id in sorted(groups, key=group_key):
        yield sorted(groups[group_id], key=order_key)
