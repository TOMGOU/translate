from PyQt5.QtWidgets import (QWidget, QLabel, QComboBox, QApplication)
import sys

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):      

        self.lbl = QLabel("Ubuntu", self)
        combo = QComboBox(self)
        combo.addItems(['中文:zh', '英语:en', '日语:jp', '韩语:kor', '法语:fra', '西班牙语:spa'])
        combo.move(50, 50)
        self.lbl.move(50, 150)
        combo.activated[str].connect(self.onActivated)        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QComboBox')
        self.show()


    def onActivated(self, text):

        self.lbl.setText(text)
        self.lbl.adjustSize()  


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())