from typing import Any, Callable, Generator, Optional, TypedDict, Union

from pydantic import Field

from app_model._pydantic_compat import model_validator

from ._base import _BaseModel


class Icon(_BaseModel):
    """Icons used to represent commands, or submenus.

    May provide both a light and dark variant.  If only one is provided, it is used
    in all theme types.
    """

    dark: Optional[str] = Field(
        None,
        description="Icon path when a dark theme is used. These may be superqt "
        "fonticon keys, such as `fa6s.arrow_down`",
    )
    light: Optional[str] = Field(
        None,
        description="Icon path when a light theme is used. These may be superqt "
        "fonticon keys, such as `fa6s.arrow_down`",
    )

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., Any], None, None]:
        yield cls._validate

    @classmethod
    def _validate(cls, v: Any) -> "Icon":
        """Validate icon."""
        # if a single string is passed, use it for both light and dark.
        if isinstance(v, Icon):
            return v
        if isinstance(v, str):
            v = {"dark": v, "light": v}
        return cls(**v)

    # for v2
    @model_validator(mode="wrap")
    @classmethod
    def _model_val(cls, v: Any, handler: Callable[[Any], "Icon"]) -> "Icon":
        if isinstance(v, str):
            v = {"dark": v, "light": v}
        return handler(v)


class IconDict(TypedDict):
    """Icon dictionary."""

    dark: Optional[str]
    light: Optional[str]


IconOrDict = Union[Icon, IconDict]
