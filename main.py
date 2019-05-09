from mainwindow import MyMainWindow
from PyQt5.QtWidgets import QApplication
from sys import argv

app = QApplication(argv)
window = MyMainWindow()
window.show()
exit(app.exec_())
