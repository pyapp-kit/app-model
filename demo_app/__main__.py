from demo_app.app import MyApp
from qtpy.QtWidgets import QApplication

qapp = QApplication([])
app = MyApp()
app.show()
qapp.exec_()
