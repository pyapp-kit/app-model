from __future__ import annotations

from typing import Callable, Dict, Iterator, List, Optional, Sequence, Set, Tuple

from psygnal import Signal

from ..types import MenuIdStr, MenuItem, MenuOrSubmenu
from ..types._constants import DisposeCallable


class MenusRegistry:
    """Registry for menu and submenu items."""

    menus_changed = Signal(set)

    def __init__(self) -> None:
        self._menu_items: Dict[MenuIdStr, List[MenuOrSubmenu]] = {}

    def append_menu_items(
        self, items: Sequence[Tuple[MenuIdStr, MenuOrSubmenu]]
    ) -> DisposeCallable:
        """Append menu items to the registry.

        Parameters
        ----------
        items : Sequence[Tuple[MenuIdStr, MenuOrSubmenu]]
            Items to append.

        Returns
        -------
        DisposeCallable
            A function that can be called to unregister the menu items.
        """
        changed_ids: Set[MenuIdStr] = set()
        disposers: List[Callable[[], None]] = []

        for id, item in items:
            item = MenuItem.validate(item)  # type: ignore
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

    def get_menu(self, menu_id: MenuIdStr) -> List[MenuOrSubmenu]:
        """Return menu items for `menu_id`."""
        return self._menu_items[menu_id]

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"<{name} at {hex(id(self))} ({len(self._menu_items)} menus)>"

    def __str__(self) -> str:
        return "\n".join(self._render())

    def _render(self) -> List[str]:
        """Return registered menu items as lines of strings."""
        # this is mostly here as a debugging tool.  Can be removed or improved later.
        lines: List[str] = []

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

    def iter_menu_groups(self, menu_id: MenuIdStr) -> Iterator[List[MenuOrSubmenu]]:
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
    items: List[MenuOrSubmenu],
    group_key: Callable = lambda x: "0000" if x == "navigation" else x,
    order_key: Callable = lambda x: getattr(x, "order", "") or 0,
) -> Iterator[List[MenuOrSubmenu]]:
    """Sort a list of menu items based on their .group and .order attributes."""
    groups: dict[Optional[str], List[MenuOrSubmenu]] = {}
    for item in items:
        groups.setdefault(item.group, []).append(item)

    for group_id in sorted(groups, key=group_key):
        yield sorted(groups[group_id], key=order_key)
