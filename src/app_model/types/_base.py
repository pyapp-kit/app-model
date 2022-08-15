from pydantic import BaseModel, Extra


class _BaseModel(BaseModel):
    """Base model for all types."""

    class Config:
        # don't switch to exclude ... it makes it hard to add fields to the
        # schema without breaking backwards compatibility
        extra = Extra.ignore
        frozen = True
