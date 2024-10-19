from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *


class dlgSelField(QDialog):
    def __init__(self, myFieldsNames, parent=None):
        QDialog.__init__(self)
        gr = QGroupBox(self)
        vbox = QVBoxLayout(gr)
        names = myFieldsNames
        self.rbl = [QRadioButton(name, gr) for name in names]
        self.rbl[0].setChecked(True)
        for rb in self.rbl:
            vbox.addWidget(rb)
        gr.adjustSize()

        hbox = QHBoxLayout()
        pbnYes = QPushButton("Yes", self)
        pbnCancel = QPushButton("Cancel", self)
        hbox.addWidget(pbnYes)
        hbox.addWidget(pbnCancel)

        layout = QVBoxLayout(self)
        layout.addWidget(gr)
        layout.addLayout(hbox)

        pbnYes.clicked.connect(self.accept)
        pbnCancel.clicked.connect(self.reject)

    def selectedAttr(self):
        for rb in self.rbl:
            if rb.isChecked():
                return rb.text()
