import runpy
from pathlib import Path

import pytest
from qtpy.QtWidgets import QApplication

DEMO = Path(__file__).parent.parent.parent / "demo"


@pytest.mark.parametrize("fname", ["qapplication.py", "model_app.py", "multi_file"])
def test_qapp(qapp, fname, monkeypatch) -> None:
    monkeypatch.setattr(QApplication, "exec", lambda *a, **k: None)
    runpy.run_path(str(DEMO / fname), run_name="__main__")
