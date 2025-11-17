from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QSlider, QSpinBox

from PyQt5.QtCore import Qt

class ValueDialog(QDialog):
    def __init__(self, title, vmin, vmax, vnow):
        super().__init__()

        self.setWindowTitle(title)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.vlayout = QVBoxLayout()

        self.hlayout = QHBoxLayout()

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(vmin)
        self.slider.setMaximum(vmax)
        self.slider.setValue(vnow)

        self.spinbox = QSpinBox()
        self.spinbox.setMinimum(vmin)
        self.spinbox.setMaximum(vmax)
        self.spinbox.setValue(vnow)

        self.slider.sliderReleased.connect(self.updateSpinBox)
        # your code

        self.hlayout.addWidget(self.spinbox)
        self.hlayout.addWidget(self.slider)

        self.vlayout.addLayout(self.hlayout)
        self.vlayout.addWidget(self.buttonBox)
        self.setLayout(self.vlayout)

    def updateSpinBox(self):
        self.spinbox.setValue(self.slider.value())

    def updateSlider(self):
        self.slider.setValue(self.spinbox.value())

    def get_value(self):
        return self.slider.value() # the value of any of either of the widgets does the job here
