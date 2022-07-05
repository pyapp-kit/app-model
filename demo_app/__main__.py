from qtpy.QtWidgets import QApplication
from .app import MyApp

qapp = QApplication([])
app = MyApp()
app.show()
qapp.exec_()
