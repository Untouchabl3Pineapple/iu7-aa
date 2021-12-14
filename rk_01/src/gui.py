from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QMessageBox, QTableWidgetItem)



class TableOfValues(QTableWidget):
    def __init__(self, values, *args):
        QTableWidget.__init__(self, *args[:2])
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.setHorizontalHeaderLabels([*args[2]])
        
        self.data = values
        self.setData()

    def update(self, newValues):
        self.data = newValues
        self.setData()

    def setData(self):
        self.setRowCount(len(self.data))
        for i, row in enumerate(self.data):
            itemX = QTableWidgetItem(row[0])
            itemY = QTableWidgetItem(row[1])
            self.setItem(i, 0, itemX)
            self.setItem(i, 1, itemY)


class GUI(QDialog):

    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)

        self.numOfRows = 10
        self.numOfCols = 2
        self.tableBoxHeader = "Expression values"
        self.formBoxHeader = "Enter yout expression"
        self.tableHeaderLabels = ['X', 'Result']
        self.buttonLabel = "Enter your expression"
        self.timeout = 2000
        self.userForm = { "func": "", "lbound": "", "rbound": "", "step": ""}
        self.RPNExpression = "No expression"

        self.initData = []

        self.tableTimer = QTimer()
        self.tableTimer.timeout.connect(self.updateAll)

        self.tableTimer.start(self.timeout)

        self.createTableBox()
        self.createFormBox()

        mainLayout = QGridLayout()

        mainLayout.addWidget(self.tableGroupBox, 0, 0)
        mainLayout.addWidget(self.formGroupBox, 0, 1)

        self.setLayout(mainLayout)

    def createTableBox(self):
        self.tableGroupBox = QGroupBox(self.tableBoxHeader)

        self.exprLabel = QLabel(self.RPNExpression)

        self.table = TableOfValues(self.initData, self.numOfRows, self.numOfCols, self.tableHeaderLabels)

        layout = QVBoxLayout()

        layout.addWidget(self.exprLabel)
        layout.addWidget(self.table)
        self.tableGroupBox.setLayout(layout)

    def createFormBox(self):
        self.formGroupBox = QGroupBox(self.formBoxHeader)

        self.functionPrompt = QLineEdit()
        self.leftBoundPrompt = QLineEdit()
        self.rightBoundPrompt = QLineEdit()
        self.stepPrompt = QLineEdit()
        self.precisionPrompt = QLineEdit()
        self.button = QPushButton(self.buttonLabel)
        self.button.clicked.connect(self.processFunction)
        
        labels = ["Expression", "Precision", "Left bound", "Right bound", "Step"]

        QLabels = [QLabel(label) for label in labels]

        layout = QGridLayout()
        layout.addWidget(QLabels[0], 0, 0, 1, 2)
        layout.addWidget(QLabels[1], 0, 2, 1, 2)
        layout.addWidget(self.functionPrompt, 1, 0, 1, 2)
        layout.addWidget(self.precisionPrompt, 1, 2, 1, 1)
        layout.addWidget(QLabels[2], 2, 0)
        layout.addWidget(QLabels[3], 2, 1)
        layout.addWidget(QLabels[4], 2, 2)
        layout.addWidget(self.leftBoundPrompt, 3, 0)
        layout.addWidget(self.rightBoundPrompt, 3, 1)
        layout.addWidget(self.stepPrompt, 3, 2)
        layout.addWidget(self.button, 4, 0, 1, 2)
        self.formGroupBox.setLayout(layout)
