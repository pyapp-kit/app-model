import gc
from unittest.mock import Mock

import pytest

from app_model.context import Context, create_context, get_context
from app_model.context._context import _OBJ_TO_CONTEXT


def test_create_context():
    """You can create a context for any object"""

    class T:
        ...

    t = T()
    tid = id(t)
    ctx = create_context(t)
    assert get_context(t) == ctx
    assert hash(ctx)  # hashable
    assert tid in _OBJ_TO_CONTEXT
    _OBJ_TO_CONTEXT.pop(tid)

    del t
    gc.collect()
    assert tid not in _OBJ_TO_CONTEXT

    # you can provide your own root, but it must be a context
    create_context(T(), root=Context())
    with pytest.raises(AssertionError):
        create_context(T(), root={})  # type: ignore


def test_create_and_get_scoped_contexts():
    """Test that objects created in the stack of another contexted object.

    likely the most common way that this API will be used:
    """
    before = len(_OBJ_TO_CONTEXT)

    class A:
        def __init__(self) -> None:
            create_context(self)
            self.b = B()

    class B:
        def __init__(self) -> None:
            create_context(self)

    obja = A()
    assert len(_OBJ_TO_CONTEXT) == before + 2
    ctxa = get_context(obja)
    ctxb = get_context(obja.b)
    assert ctxa is not None
    assert ctxb is not None
    ctxa["hi"] = "hi"
    assert ctxb["hi"] == "hi"

    # keys get deleted on object deletion
    del obja
    gc.collect()
    assert len(_OBJ_TO_CONTEXT) == before


def test_context_events():
    """Changing context keys emits an event"""
    mock = Mock()
    root = Context()
    scoped = root.new_child()
    scoped.changed.connect(mock)  # connect the mock to the child

    root["a"] = 1
    # child re-emits parent events
    assert mock.call_args[0][0] == {"a"}

    mock.reset_mock()
    scoped["b"] = 1
    # also emits own events
    assert mock.call_args[0][0] == {"b"}

    mock.reset_mock()
    del scoped["b"]
    assert mock.call_args[0][0] == {"b"}

    # but parent does not emit child events
    mock.reset_mock()
    mock2 = Mock()
    root.changed.connect(mock2)
    scoped["c"] = "c"
    mock.assert_called_once()
    mock2.assert_not_called()
