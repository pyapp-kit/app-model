"""https://www.mkdocs.org/dev-guide/plugins/#events ."""
from __future__ import annotations

import importlib.abc
from importlib import import_module
from importlib.machinery import ModuleSpec
from textwrap import dedent
from typing import TYPE_CHECKING, Any

from griffe.dataclasses import Alias
from mkdocstrings_handlers.python.handler import PythonHandler

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence
    from types import ModuleType

    from mkdocstrings.handlers.base import CollectorItem


def inject_dynamic_docstring(item: Alias, identifier: str) -> None:
    module, name = identifier.rsplit(".", 1)
    obj = getattr(import_module(module), name)
    first_line, *rest = (obj.__doc__ or "").splitlines()
    if first_line and item.target.docstring:
        item.target.docstring.value = first_line + "\n" + dedent("\n".join(rest))


class AppModelHandler(PythonHandler):
    def collect(self, identifier: str, config: Mapping[str, Any]) -> CollectorItem:
        item = super().collect(identifier, config)
        if isinstance(item, Alias):
            inject_dynamic_docstring(item, identifier)
        # to edit default in the parameter table
        # item.parameters["something"].default = ...
        return item


class MyLoader(importlib.abc.Loader):
    def exec_module(self, module: ModuleType) -> None:
        def get_handler(
            theme: str,
            custom_templates: str | None = None,
            config_file_path: str | None = None,
            **config: Any,
        ) -> PythonHandler:
            paths = config.get("paths", [])
            locale = config.get("locale", None)
            load_external_modules = config.get("load_external_modules", False)
            # breakpoint()
            return PythonHandler(
                handler="python",
                theme=theme,
                custom_templates=custom_templates,
                config_file_path=config_file_path,
                paths=paths,
                locale=locale,
                load_external_modules=load_external_modules,
            )

            # return AppModelHandler(handler="python", *args, **kwargs)
            # return PythonHandler(handler="python", *args, **kwargs)

        module.get_handler = get_handler  # type: ignore


class Finder(importlib.abc.MetaPathFinder):
    def find_spec(
        self,
        fullname: str,
        path: Sequence[str] | None,
        target: ModuleType | None = None,
    ) -> ModuleSpec | None:
        if fullname == "mkdocstrings_handlers.app_model":
            return ModuleSpec(fullname, MyLoader())
        return None
