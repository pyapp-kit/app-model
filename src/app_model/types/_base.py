from typing import TYPE_CHECKING, ClassVar

from pydantic_compat import BaseModel

if TYPE_CHECKING:
    from pydantic import ConfigDict


class _BaseModel(BaseModel):
    """Base model for all types."""

    # don't switch to exclude ... it makes it hard to add fields to the
    # schema without breaking backwards compatibility
    model_config: ClassVar["ConfigDict"] = {"frozen": True, "extra": "ignore"}
