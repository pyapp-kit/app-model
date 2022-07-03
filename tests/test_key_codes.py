import pytest

from app_model.types._keys import KeyChord, KeyCode, KeyMod, ScanCode, SimpleKeyBinding


def test_key_codes():
    for key in KeyCode:
        assert key == KeyCode.from_string(str(key))

    assert KeyCode.from_event_code(65) == KeyCode.KeyA

    assert KeyCode.validate(int(KeyCode.KeyA)) == KeyCode.KeyA
    assert KeyCode.validate(KeyCode.KeyA) == KeyCode.KeyA
    assert KeyCode.validate("A") == KeyCode.KeyA

    with pytest.raises(TypeError, match="cannot convert"):
        KeyCode.validate({"a"})


def test_scan_codes():
    for scan in ScanCode:
        assert scan == ScanCode.from_string(str(scan)), scan


def test_key_combo():
    """KeyCombo is an integer combination of one or more KeyMod and KeyCode."""
    combo = KeyMod.Shift | KeyMod.Alt | KeyCode.KeyK
    assert repr(combo) == "<KeyCombo.Shift|Alt|KeyK: 1564>"
    kb = SimpleKeyBinding.from_int(combo)
    assert kb == SimpleKeyBinding(shift=True, alt=True, key=KeyCode.KeyK)


def test_key_chord():
    """KeyChord is an integer combination of two KeyCombos, KeyCodes, or integers."""
    chord = KeyChord(KeyMod.CtrlCmd | KeyCode.KeyK, KeyCode.KeyM)
    assert int(chord) == 1968156
    assert repr(chord) == "KeyChord(<KeyCombo.CtrlCmd|KeyK: 2076>, <KeyCode.KeyM: 30>)"
