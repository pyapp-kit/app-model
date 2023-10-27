from typing import Any, Callable, Generator, Optional, TypedDict, Union

from pydantic import Field

from app_model._pydantic_compat import model_validator

from ._base import _BaseModel

LIGHT_COLOR = "#BCB4B4"
DARK_COLOR = "#6B6565"


class Icon(_BaseModel):
    """Icons used to represent commands, or submenus.

    May provide both a light and dark variant.  If only one is provided, it is used
    in all theme types.
    """

    dark: Optional[str] = Field(
        None,
        description="Icon path when a dark theme is used. These may be "
        "[iconify keys](https://icon-sets.iconify.design), such as `mdi:content-copy`, "
        "or [superqt.fonticon](https://pyapp-kit.github.io/superqt/utilities/fonticon/)"
        " keys, such as `fa6s.arrow_down`",
    )
    color_dark: Optional[str] = Field(
        LIGHT_COLOR,  # use light icon for dark themes
        description="Icon color to use for themes with dark backgrounds. If not "
        "provided, a default is used.",
    )
    light: Optional[str] = Field(
        None,
        description="Icon path when a light theme is used. These may be "
        "[iconify keys](https://icon-sets.iconify.design), such as `mdi:content-copy`, "
        "or [superqt.fonticon](https://pyapp-kit.github.io/superqt/utilities/fonticon/)"
        " keys, such as `fa6s.arrow_down`",
    )
    color_light: Optional[str] = Field(
        DARK_COLOR,  # use dark icon for light themes
        description="Icon color to use for themes with light backgrounds. If not "
        "provided, a default is used",
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
        if isinstance(v, dict):
            if "dark" in v:
                v.setdefault("light", v["dark"])
            elif "light" in v:
                v.setdefault("dark", v["light"])
        return cls(**v)

    # for v2
    @model_validator(mode="wrap")
    @classmethod
    def _model_val(cls, v: Any, handler: Callable[[Any], "Icon"]) -> "Icon":
        if isinstance(v, str):
            v = {"dark": v, "light": v}
        if isinstance(v, dict):
            if "dark" in v:
                v.setdefault("light", v["dark"])
            elif "light" in v:
                v.setdefault("dark", v["light"])
        return handler(v)


class IconDict(TypedDict):
    """Icon dictionary."""

    dark: Optional[str]
    light: Optional[str]
    color_dark: Optional[str]
    color_light: Optional[str]


IconOrDict = Union[Icon, IconDict]
