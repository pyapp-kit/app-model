from posixpath import split
from typing import TYPE_CHECKING
from importlib import import_module

from pydantic import BaseModel

if TYPE_CHECKING:
    from mkdocs_macros.plugin import MacrosPlugin


def _import_attr(name: str):
    mod, attr = name.rsplit(".", 1)
    return getattr(import_module(mod), attr)


def define_env(env: "MacrosPlugin"):
    @env.macro
    def pydantic_table(name: str):
        cls = _import_attr(name)
        assert issubclass(cls, BaseModel)
        rows = ["| Field | Type | Description |", "| ----  | ---- | ----------- |"]
        for f in cls.__fields__.values():
            mod = f.type_.__module__ + '.' if f.type_.__module__ != 'builtins' else ''
            type_fullpath = f"{mod}{f.type_.__name__}"
            type_ = f"[`{f.type_.__name__}`][{type_fullpath}]"
            row = f"| {f.name} | {type_} | {f.field_info.description} |"
            rows.append(row)
        return "\n".join(rows)
