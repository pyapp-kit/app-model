import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent))

from qtpy.QtWidgets import QApplication

from multi_file.app import MyApp

qapp = QApplication.instance() or QApplication([])
app = MyApp()
app.show()
qapp.exec_()
