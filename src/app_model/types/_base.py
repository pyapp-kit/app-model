from pydantic import BaseModel, __version__

PYDANTIC2 = __version__.startswith("2")


class _BaseModel(BaseModel):
    """Base model for all types."""

    if PYDANTIC2:
        model_config = {"extra": "ignore", "frozen": True}
    else:

        class Config:
            # don't switch to exclude ... it makes it hard to add fields to the
            # schema without breaking backwards compatibility
            extra = "ignore"
            frozen = True
