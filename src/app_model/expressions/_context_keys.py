from __future__ import annotations

import contextlib
from types import MappingProxyType
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Generic,
    Literal,
    MutableMapping,
    NamedTuple,
    TypeVar,
    overload,
)

from ._expressions import Name

if TYPE_CHECKING:
    import builtins

T = TypeVar("T")
A = TypeVar("A")


class __missing:
    """Sentinel... done this way for the purpose of typing."""

    def __repr__(self) -> str:
        return "MISSING"


MISSING = __missing()


class ContextKeyInfo(NamedTuple):
    """Just a recordkeeping tuple.

    Retrieve all declared ContextKeys with ContextKeyInfo.info().
    """

    key: str
    type: type | None
    description: str | None
    namespace: builtins.type[ContextNamespace] | None


class ContextKey(Name, Generic[A, T]):
    """Context key name, default, description, and getter.

    This is intended to be used as class attribute in a `ContextNamespace`.
    This is a subclass of `Name`, and is therefore usable in an `Expression`.
    (see examples.)

    Parameters
    ----------
    default_value : Any, optional
        The default value for this key, by default MISSING
    description : str, optional
        Description of this key.  Useful for documentation, by default None
    getter : callable, optional
        Callable that receives an object and retrieves the current value for
        this key, by default None.
        For example, if this ContextKey represented the length of some list,
        (like the layerlist) it might look like
        `length = ContextKey(0, 'length of the list', lambda x: len(x))`
    id : str, optional
        Explicitly provide the `Name` string used when evaluating a context,
        by default the key will be taken as the attribute name to which this
        object is assigned as a class attribute:

    Examples
    --------
    >>> class MyNames(ContextNamespace):
    ...     some_key = ContextKey(0, "some description", lambda x: sum(x))

    >>> expr = MyNames.some_key > 5  # create an expression using this key

    these expressions can be later evaluated with some concrete context.

    >>> expr.eval({"some_key": 3})  # False
    >>> expr.eval({"some_key": 6})  # True
    """

    # This will catalog all ContextKeys that get instantiated, which provides
    # an easy way to organize documentation.
    # ContextKey.info() returns a list with info for all ContextKeys
    _info: ClassVar[list[ContextKeyInfo]] = []
    MISSING = MISSING

    def __init__(
        self,
        default_value: T | __missing = MISSING,
        description: str | None = None,
        getter: Callable[[A], T] | None = None,
        *,
        id: str = "",  # optional because of __set_name__
    ) -> None:
        super().__init__(id or "")
        self._default_value = default_value
        self._getter = getter
        self._description = description
        self._owner: type[ContextNamespace] | None = None
        self._type = (
            type(default_value) if default_value not in (None, MISSING) else None
        )
        if id:
            self._store()

    def __str__(self) -> str:
        return self.id

    @classmethod
    def info(cls) -> list[ContextKeyInfo]:
        """Return list of all stored context keys."""
        return list(cls._info)

    def _store(self) -> None:
        self._info.append(
            ContextKeyInfo(self.id, self._type, self._description, self._owner)
        )

    def __set_name__(self, owner: type[ContextNamespace[A]], name: str) -> None:
        """Set the name for this key.

        (this happens when you instantiate this class as a class attribute).
        """
        if self.id:
            raise RuntimeError(
                f"Cannot change id of ContextKey (already {self.id!r})",
            )
        self._owner = owner
        self.id = name
        # recompile the code with the new name
        self._recompile()
        self._store()

    @overload
    def __get__(self, obj: Literal[None], objtype: type) -> ContextKey[A, T]:
        # When we __get__ from the class, we return ourself
        ...

    @overload
    def __get__(self, obj: ContextNamespace[A], objtype: type) -> T:
        # When we got from the object, we return the current value
        ...

    def __get__(
        self, obj: ContextNamespace[A] | None, objtype: type
    ) -> T | ContextKey[A, T] | None:
        """Get current value of the key in the associated context."""
        return self if obj is None else obj._context.get(self.id, MISSING)

    def __set__(self, obj: ContextNamespace[A], value: T) -> None:
        """Set current value of the key in the associated context."""
        obj._context[self.id] = value

    def __delete__(self, obj: ContextNamespace[A]) -> None:
        """Delete key from the associated context."""
        del obj._context[self.id]


class ContextNamespaceMeta(type):
    """Metaclass that finds all ContextNamespace members."""

    _members_map_: dict[str, ContextKey]

    def __new__(cls, clsname: str, bases: tuple, attrs: dict) -> ContextNamespaceMeta:
        """Create a new ContextNamespace class."""
        new_cls = super().__new__(cls, clsname, bases, attrs)
        new_cls._members_map_ = {
            k: v for k, v in attrs.items() if isinstance(v, ContextKey)
        }
        return new_cls

    @property
    def __members__(self) -> MappingProxyType[str, ContextKey]:
        return MappingProxyType(self._members_map_)

    def __dir__(self) -> list[str]:  # pragma: no cover
        return [
            "__class__",
            "__doc__",
            "__members__",
            "__module__",
            *list(self._members_map_),
        ]


class ContextNamespace(Generic[A], metaclass=ContextNamespaceMeta):
    """A collection of related keys in a context.

    meant to be subclassed, with `ContextKeys` as class attributes.
    """

    def __init__(self, context: MutableMapping) -> None:
        self._context = context

        # on instantiation we create an index of defaults and value-getters
        # to speed up retrieval later
        self._defaults: dict[str, Any] = {}  # default values per key
        self._getters: dict[str, Callable[[A], Any]] = {}  # value getters
        for name, ctxkey in type(self).__members__.items():
            self._defaults[name] = ctxkey._default_value
            if ctxkey._default_value is not MISSING:
                context[ctxkey.id] = ctxkey._default_value
            if callable(ctxkey._getter):
                self._getters[name] = ctxkey._getter

    def reset(self, key: str) -> None:
        """Reset keys to its default."""
        val = self._defaults[key]
        if val is MISSING:
            with contextlib.suppress(KeyError):
                delattr(self, key)
        else:
            setattr(self, key, self._defaults[key])

    def reset_all(self) -> None:
        """Reset all keys to their defaults."""
        for key in self._defaults:
            self.reset(key)

    def dict(self) -> dict:
        """Return all keys in this namespace."""
        return {k: getattr(self, k) for k in type(self).__members__}

    def __repr__(self) -> str:
        import pprint

        return pprint.pformat(self.dict())
