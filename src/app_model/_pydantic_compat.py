from pydantic import BaseModel, __version__

PYDANTIC2 = __version__.startswith("2")

if PYDANTIC2:
    from pydantic import field_validator

    def validator(*args, **kwargs):
        return field_validator(*args, **kwargs)

    def asdict(obj: BaseModel, *args, **kwargs):
        return obj.model_dump(*args, **kwargs)

    def asjson(obj: BaseModel, *args, **kwargs):
        return obj.model_dump_json(*args, **kwargs)

else:
    from pydantic import validator as validator  # noqa

    def asdict(obj: BaseModel, *args, **kwargs):
        return obj.dict(*args, **kwargs)

    def asjson(obj: BaseModel, *args, **kwargs):
        return obj.json(*args, **kwargs)
