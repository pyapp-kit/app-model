import pytest

from app_model.registries import CommandsRegistry, RegisteredCommand


def raise_exc() -> None:
    raise RuntimeError("boom")


def test_commands_registry() -> None:
    reg = CommandsRegistry()
    id1 = "my.id"
    reg.register_command(id1, lambda: 42, "My Title")
    assert "(1 commands)" in repr(reg)
    assert id1 in str(reg)
    assert id1 in reg
    with pytest.raises(KeyError, match="my.id2"):
        reg["my.id2"]

    with pytest.raises(ValueError, match="Command 'my.id' already registered"):
        reg.register_command(id1, lambda: 42, "My Title")

    assert reg.execute_command(id1, execute_asynchronously=True).result() == 42
    assert reg.execute_command(id1, execute_asynchronously=False).result() == 42

    reg.register_command("my.id2", raise_exc, "My Title 2")
    future_async = reg.execute_command("my.id2", execute_asynchronously=True)
    future_sync = reg.execute_command("my.id2", execute_asynchronously=False)

    with pytest.raises(RuntimeError, match="boom"):
        future_async.result()
    with pytest.raises(RuntimeError, match="boom"):
        future_sync.result()


def test_commands_raises() -> None:
    reg = CommandsRegistry(raise_synchronous_exceptions=True)

    id_ = "my.id"
    title = "My Title"
    reg.register_command(id_, raise_exc, title)

    with pytest.raises(RuntimeError, match="boom"):
        reg.execute_command(id_)

    cmd = reg[id_]
    assert isinstance(cmd, RegisteredCommand)
    assert cmd.title == title

    with pytest.raises(AttributeError, match="immutable"):
        cmd.title = "New Title"

    assert cmd.title == title
