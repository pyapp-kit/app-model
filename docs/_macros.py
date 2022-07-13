import collections.abc
from importlib import import_module
from typing import TYPE_CHECKING, Any, TypeVar, Union

from pydantic import BaseModel
from typing_extensions import ParamSpec

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
            type_ = _build_type_link(f.outer_type_)
            row = f"| {f.name} | {type_} | {f.field_info.description} |"
            rows.append(row)
        return "\n".join(rows)


def _type_link(typ: Any) -> str:
    mod = f"{typ.__module__}." if typ.__module__ != "builtins" else ""
    type_fullpath = f"{mod}{typ.__name__}"
    return f"[`{typ.__name__}`][{type_fullpath}]"


def _build_type_link(typ: Any) -> str:
    origin = getattr(typ, "__origin__", None)
    if origin is None:
        return _type_link(typ)

    args = getattr(typ, "__args__", ())
    if origin is collections.abc.Callable and any(
        isinstance(a, (TypeVar, ParamSpec)) for a in args
    ):
        return _type_link(origin)
    types = [_build_type_link(a) for a in args if a is not type(None)]  # noqa
    if origin is Union:
        return " or ".join(types)
    type_ = ", ".join(types)
    return f"{_type_link(origin)}[{type_}]"
