import sys

from qtpy.QtWidgets import QApplication

from app_model.backends.qt import QModelKeyBindingEdit

app = QApplication(sys.argv)
w = QModelKeyBindingEdit()
w.editingFinished.connect(lambda: print(w.keyBinding()))
w.show()
sys.exit(app.exec_())
