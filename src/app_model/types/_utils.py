import re
from importlib import import_module
from typing import Any

_identifier_plus_dash = "(?:[a-zA-Z_][a-zA-Z_0-9-]+)"
_dotted_name = f"(?:(?:{_identifier_plus_dash}\\.)*{_identifier_plus_dash})"
PYTHON_NAME_PATTERN = re.compile(f"^({_dotted_name}):({_dotted_name})$")


def _validate_python_name(name: str) -> str:
    """Assert that `name` is a valid python name: e.g. `module.submodule:funcname`."""
    if name and not PYTHON_NAME_PATTERN.match(name):
        msg = (
            f"{name!r} is not a valid python_name. A python_name must "
            "be of the form '{obj.__module__}:{obj.__qualname__}' (e.g. "
            "'my_package.a_module:some_function')."
        )
        if ".<locals>." in name:  # pragma: no cover
            *_, a, b = name.split(".<locals>.")
            a = a.split(":")[-1]
            msg += (
                " Note: functions defined in local scopes are not yet supported. "
                f"Please move function {b!r} to the global scope of module {a!r}"
            )
        raise ValueError(msg)
    return name


def import_python_name(python_name: str) -> Any:
    """Import object from a fully qualified python name.

    Examples
    --------
    >>> import_python_name("my_package.a_module:some_function")
    <function some_function at 0x...>
    >>> import_python_name("pydantic:BaseModel")
    <class 'pydantic.main.BaseModel'>
    """
    _validate_python_name(python_name)  # shows the best error message
    if match := PYTHON_NAME_PATTERN.match(python_name):
        module_name, funcname = match.groups()
        mod = import_module(module_name)
        return getattr(mod, funcname)
    raise ValueError(  # pragma: no cover
        f"Could not parse python_name: {python_name!r}"
    )
