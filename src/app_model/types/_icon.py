from typing import Any, TypeAlias, TypedDict

from pydantic import Field, model_validator

from ._base import _BaseModel


class Icon(_BaseModel):
    """Icons used to represent commands, or submenus.

    May provide both a light and dark variant.  If only one is provided, it is used
    in all theme types.
    """

    dark: str | None = Field(
        default=None,
        description="Icon path when a dark theme is used. These may be "
        "[iconify keys](https://icon-sets.iconify.design), such as "
        "`fa6-solid:arrow-down`, or "
        "[superqt.fonticon](https://pyapp-kit.github.io/superqt/utilities/fonticon/)"
        " keys, such as `fa6s.arrow_down`",
    )
    color_dark: str | None = Field(
        None,  # use light icon for dark themes
        description="(Light) icon color to use for themes with dark backgrounds. "
        "If not provided, a default is used.",
    )
    light: str | None = Field(
        default=None,
        description="Icon path when a light theme is used. These may be "
        "[iconify keys](https://icon-sets.iconify.design), such as "
        "`fa6-solid:arrow-down`, or "
        "[superqt.fonticon](https://pyapp-kit.github.io/superqt/utilities/fonticon/)"
        " keys, such as `fa6s.arrow_down`",
    )
    color_light: str | None = Field(
        None,  # use dark icon for light themes
        description="(Dark) icon color to use for themes with light backgrounds. "
        "If not provided, a default is used",
    )

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
    @model_validator(mode="before")
    @classmethod
    def _model_val(cls, v: dict) -> dict:
        if isinstance(v, str):
            v = {"dark": v, "light": v}
        if isinstance(v, dict):
            if "dark" in v:
                v.setdefault("light", v["dark"])
            elif "light" in v:
                v.setdefault("dark", v["light"])
        return v


class IconDict(TypedDict):
    """Icon dictionary."""

    dark: str | None
    light: str | None
    color_dark: str | None
    color_light: str | None


IconOrDict: TypeAlias = Icon | IconDict
