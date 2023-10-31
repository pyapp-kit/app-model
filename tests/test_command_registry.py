import pytest

from app_model.registries import CommandsRegistry


def raise_exc() -> None:
    raise RuntimeError("boom")


def test_commands_registry() -> None:
    reg = CommandsRegistry()
    reg.register_command("my.id", lambda: 42, "My Title")
    assert "(1 commands)" in repr(reg)
    assert "my.id" in str(reg)
    assert "my.id" in reg
    with pytest.raises(KeyError, match="my.id2"):
        reg["my.id2"]

    with pytest.raises(ValueError, match="Command 'my.id' already registered"):
        reg.register_command("my.id", lambda: 42, "My Title")

    assert reg.execute_command("my.id", execute_asynchronously=True).result() == 42
    assert reg.execute_command("my.id", execute_asynchronously=False).result() == 42

    reg.register_command("my.id2", raise_exc, "My Title 2")
    future_async = reg.execute_command("my.id2", execute_asynchronously=True)
    future_sync = reg.execute_command("my.id2", execute_asynchronously=False)

    with pytest.raises(RuntimeError, match="boom"):
        future_async.result()
    with pytest.raises(RuntimeError, match="boom"):
        future_sync.result()


def test_commands_raises() -> None:
    reg = CommandsRegistry(raise_synchronous_exceptions=True)

    reg.register_command("my.id", raise_exc, "My Title")

    with pytest.raises(RuntimeError, match="boom"):
        reg.execute_command("my.id")
