from __future__ import annotations

import sys
from contextlib import contextmanager
from types import FrameType
from typing import (
    Any,
    Callable,
    ChainMap,
    Dict,
    Iterator,
    MutableMapping,
    Optional,
    Type,
)
from weakref import finalize

from psygnal import Signal

_null = object()


class Context(ChainMap):
    """Evented Mapping of keys to values."""

    changed = Signal(set)  # Set[str]

    @contextmanager
    def buffered_changes(self) -> Iterator[None]:
        """Context in which to accumulated changes before emitting."""
        with self.changed.paused(lambda a, b: (a[0].union(b[0]),)):
            yield

    def __setitem__(self, k: str, v: Any) -> None:
        emit = self.get(k, _null) is not v
        super().__setitem__(k, v)
        if emit:
            self.changed.emit({k})

    def __delitem__(self, k: str) -> None:
        emit = k in self
        super().__delitem__(k)
        if emit:
            self.changed.emit({k})

    def new_child(self, m: Optional[MutableMapping] = None) -> Context:
        """Create a new child context from this one."""
        new = super().new_child(m=m)
        self.changed.connect(new.changed)
        return new

    def __hash__(self) -> int:
        return id(self)


# note: it seems like WeakKeyDictionary would be a nice match here, but
# it appears that the object somehow isn't initialized "enough" to register
# as the same object in the WeakKeyDictionary later when queried with
# `obj in _OBJ_TO_CONTEXT` ... so instead we use id(obj)
# _OBJ_TO_CONTEXT: WeakKeyDictionary[object, Context] = WeakKeyDictionary()
_OBJ_TO_CONTEXT: Dict[int, Context] = {}
_ROOT_CONTEXT: Optional[Context] = None


def _pydantic_abort(frame: FrameType) -> bool:
    # type is being declared and pydantic is checking defaults
    # this context will never be used.
    return frame.f_code.co_name in ("__new__", "_set_default_and_type")


def create_context(
    obj: object,
    max_depth: int = 20,
    start: int = 2,
    root: Optional[Context] = None,
    root_class: Type[Context] = Context,
    frame_predicate: Callable[[FrameType], bool] = _pydantic_abort,
) -> Optional[Context]:
    """Create context for any object.

    Parameters
    ----------
    obj : object
        Any object
    max_depth : int, optional
        Max frame depth to search for another object (that already has a context) off
        of which to scope this new context.  by default 20
    start : int, optional
        first frame to use in search, by default 2
    root : Optional[Context], optional
        Root context to use, by default None
    root_class : Type[Context], optional
        Root class to use when creating a global root context, by default Context
        The global context is used when root is None.
    frame_predicate : Callable[[FrameType], bool], optional
        Callback that can be used to abort context creation.  Will be called on each
        frame in the stack, and if it returns True, the context will not be created.
        by default, uses pydantic-specific function to determine if a new pydantic
        BaseModel is being *declared*, (which means that the context will never be used)
        `lambda frame: frame.f_code.co_name in ("__new__", "_set_default_and_type")`

    Returns
    -------
    Optional[Context]
        Context for the object, or None if no context was found
    """
    if root is None:
        global _ROOT_CONTEXT
        if _ROOT_CONTEXT is None:
            _ROOT_CONTEXT = root_class()
        root = _ROOT_CONTEXT
    else:
        assert isinstance(root, Context), "root must be an instance of Context"

    parent = root
    if hasattr(sys, "_getframe"):  # CPython implementation detail
        frame: Optional[FrameType] = sys._getframe(start)
        i = -1
        # traverse call stack looking for another object that has a context
        # to scope this new context off of.
        while frame and (i := i + 1) < max_depth:
            if frame_predicate(frame):
                return None  # pragma: no cover

            # FIXME: this might be a bit napari "magic"
            # it also assumes someone uses "self" as the first argument
            if "self" in frame.f_locals:
                _ctx = _OBJ_TO_CONTEXT.get(id(frame.f_locals["self"]))
                if _ctx is not None:
                    parent = _ctx
                    break
            frame = frame.f_back

    new_context = parent.new_child()
    obj_id = id(obj)
    _OBJ_TO_CONTEXT[obj_id] = new_context
    # remove key from dict when object is deleted
    finalize(obj, lambda: _OBJ_TO_CONTEXT.pop(obj_id, None))
    return new_context


def get_context(obj: object) -> Optional[Context]:
    """Return context for any object, if found."""
    return _OBJ_TO_CONTEXT.get(id(obj))
