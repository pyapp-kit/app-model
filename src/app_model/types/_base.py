from pydantic import BaseModel, Extra


class _StrictModel(BaseModel):
    class Config:
        extra = Extra.forbid
