from pydantic import BaseModel


class _BaseModel(BaseModel):
    """Base model for all types."""

    class Config:
        # don't switch to exclude ... it makes it hard to add fields to the
        # schema without breaking backwards compatibility
        extra = "ignore"
        frozen = True
