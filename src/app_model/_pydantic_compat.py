from __future__ import annotations

from typing import Any, Callable, Literal, TypeVar

from pydantic import BaseModel, __version__

PYDANTIC2 = __version__.startswith("2")
M = TypeVar("M", bound=BaseModel)
C = TypeVar("C", bound=Callable[..., Any])


# no-op for v1, put first for typing.
def model_validator(*, mode: Literal["wrap", "before", "after"]) -> Callable[[C], C]:
    def decorator(func: C) -> C:
        return func

    return decorator


if PYDANTIC2:
    from pydantic import field_validator
    from pydantic import model_validator as model_validator  # type: ignore # noqa

    def validator(*args: Any, **kwargs: Any) -> Callable[[Callable], Callable]:
        return field_validator(*args, **kwargs)

    def asdict(obj: BaseModel, *args: Any, **kwargs: Any) -> dict:
        return obj.model_dump(*args, **kwargs)

    def asjson(obj: BaseModel, *args: Any, **kwargs: Any) -> str:
        return obj.model_dump_json(*args, **kwargs)

else:
    from pydantic import validator as validator

    def asdict(obj: BaseModel, *args: Any, **kwargs: Any) -> dict:
        return obj.dict(*args, **kwargs)

    def asjson(obj: BaseModel, *args: Any, **kwargs: Any) -> str:
        return obj.json(*args, **kwargs)


def model_config(**kwargs: Any) -> dict | type:
    return kwargs if PYDANTIC2 else type("Config", (), kwargs)
