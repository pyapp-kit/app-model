from typing import TYPE_CHECKING, cast

from pydantic import BaseModel

from app_model._pydantic_compat import PYDANTIC2, model_config

if TYPE_CHECKING:
    from pydantic import ConfigDict
# don't switch to exclude ... it makes it hard to add fields to the
# schema without breaking backwards compatibility
_config = model_config(extra="ignore", frozen=True)


class _BaseModel(BaseModel):
    """Base model for all types."""

    if PYDANTIC2:
        model_config = cast("ConfigDict", _config)
    else:
        Config = _config  # type: ignore
