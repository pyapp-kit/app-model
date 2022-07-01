from pydantic import BaseModel, Extra


class _StrictModel(BaseModel):
    """Base model for all types."""

    class Config:
        extra = Extra.forbid
