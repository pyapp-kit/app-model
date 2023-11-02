"""https://www.mkdocs.org/dev-guide/plugins/#events ."""
from __future__ import annotations

import importlib.abc
import sys
import warnings
from functools import partial
from importlib import import_module
from importlib.machinery import ModuleSpec
from typing import TYPE_CHECKING, Any

from griffe.dataclasses import Alias
from mkdocstrings_handlers.python.handler import PythonHandler

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence
    from pathlib import Path
    from types import ModuleType

    from fieldz import Field
    from mkdocstrings.handlers.base import CollectorItem

warnings.simplefilter("ignore", DeprecationWarning)


def _parse_pydantic(doc, fields: tuple[Field, ...]):
    from griffe.docstrings.dataclasses import (
        DocstringAttribute,
        DocstringSectionAttributes,
    )
    from griffe.docstrings.parsers import parse

    val = parse(doc, "numpy")

    val.pop()
    val.append(
        DocstringSectionAttributes(
            [
                DocstringAttribute(
                    name=f.name,
                    # annotation=ExprName(name=f.type_display()),
                    description=f.description,
                    value=f.default,
                )
                for f in fields
            ]
        )
    )
    return val


def inject_dynamic_docstring(item: Alias, identifier: str) -> None:
    from fieldz import fields
    from pydantic import BaseModel

    module, name = identifier.rsplit(".", 1)
    try:
        obj = getattr(import_module(module), name)
        if not issubclass(obj, BaseModel):
            return
    except (ModuleNotFoundError, TypeError):
        return
    # breakpoint()
    item.target.docstring.parse = partial(
        _parse_pydantic, item.target.docstring, fields=fields(obj)
    )
    return True
    # item.target.docstring.value = "asdf"
    # return
    # if not (docstring := obj.__doc__):
    #     return
    # first_line, *rest = docstring.splitlines()
    # if first_line and item.target.docstring:
    #     item.target.docstring.value = first_line + "\n" + dedent("\n".join(rest))


class AppModelHandler(PythonHandler):
    def collect(self, identifier: str, config: Mapping[str, Any]) -> CollectorItem:
        item = super().collect(identifier, config)
        if isinstance(item, Alias):
            if inject_dynamic_docstring(item, identifier):
                try:
                    config["docstring_options"]["docstring_section_style"] = "table"
                except KeyError:
                    pass
        return item

    def get_templates_dir(self, handler: str | None = None) -> Path:
        return super().get_templates_dir("python")


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
            return AppModelHandler(
                handler="app_model",
                theme=theme,
                custom_templates=custom_templates,
                config_file_path=config_file_path,
                paths=paths,
                locale=locale,
                load_external_modules=load_external_modules,
            )

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


def on_startup(command: str, dirty: bool) -> None:
    sys.meta_path.append(Finder())
