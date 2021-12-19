from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QMessageBox, QTableWidgetItem, QHeaderView)



class TableOfValues(QTableWidget):
    def __init__(self, values, *args):
        QTableWidget.__init__(self, *args[:2])
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.setHorizontalHeaderLabels([*args[2]])
        self.setFixedWidth(400)
        
        self.data = values
        self.setData()
        self.header = self.horizontalHeader()       

    def update(self, newValues):
        self.data = newValues
        self.setData()

    def setData(self):
        self.setRowCount(len(self.data))
        for i, row in enumerate(self.data):
            for j, element in enumerate(row):
                self.header.setSectionResizeMode(j, QHeaderView.Stretch)
                item = QTableWidgetItem(element)
                self.setItem(i, j, item)


class GUI(QDialog):

    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)

        self.funcNumOfRows = 10
        self.funcNumOfCols = 2
        self.historyNumOfRows = 10
        self.historyNumOfCols = 4
        self.tableBoxHeader = "Expression values"
        self.formBoxHeader = "Enter your expression"
        self.funcTableHeaderLabels = ['X', 'Result']
        self.historyTableHeaderLabels = ['Index', 'Symbol', 'Output array', 'Stack']
        self.buttonLabel = "Enter your expression"
        self.timeout = 20000
        self.userForm = { "func": "", "lbound": "", "rbound": "", "step": ""}
        self.RPNExpression = "No expression is set"

        self.initFuncData = []
        self.initHistoryData = []

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
        self.tableGroupBox = QTabWidget()
        self.tableGroupBox.setFixedWidth(480)

        funcTab = QWidget()
        historyTab = QWidget()

        self.exprLabel = QLabel(self.RPNExpression)

        self.funcTable = TableOfValues(self.initFuncData, self.funcNumOfRows, self.funcNumOfCols, self.funcTableHeaderLabels)
        self.historyTable = TableOfValues(self.initHistoryData, self.historyNumOfRows, self.historyNumOfCols, self.historyTableHeaderLabels)

        funcTabBox = QHBoxLayout()
        funcTabBox.setContentsMargins(5, 5, 5, 5)
        funcTabBox.addWidget(self.funcTable)

        funcTab.setLayout(funcTabBox)

        historyTabBox = QHBoxLayout()
        historyTabBox.setContentsMargins(5, 5, 5, 5)
        historyTabBox.addWidget(self.historyTable)

        historyTab.setLayout(historyTabBox)

        self.tableGroupBox.addTab(funcTab, "Result")
        self.tableGroupBox.addTab(historyTab, "Element")

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
