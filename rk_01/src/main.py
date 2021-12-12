from PyQt5.QtWidgets import QApplication, QMessageBox
import unittest
from rpn import RPN, RPNException, TestRPN
from gui import GUI
import sys

class App(RPN, GUI):
    def __init__(self):
        GUI.__init__(self)
        RPN.__init__(self)

        self.functionPoints = []
        self.functionValues = []

    def processFunction(self):
        leftBound = self.leftBoundPrompt.text()
        rightBound = self.rightBoundPrompt.text()
        step = self.stepPrompt.text()
        func = self.functionPrompt.text()

        if leftBound == "":
            self.popupError("No left bound was provided!")
            return

        if rightBound == "":
            self.popupError("No right bound was provided!")
            return
        if step == "":
            self.popupError("No step was provided!")
            return
        if func == "":
            self.popupError("No function was provided!")
            return

        self.userForm["func"] = func 
        self.userForm["lbound"] = float(leftBound)
        self.userForm["rbound"] = float(rightBound)
        self.userForm["step"] = float(step)

        self.findPointsInRange()

        self.generateFunctionTable()

        self.updateAll()

    def findPointsInRange(self):
        cur = self.userForm["lbound"]
        rbound = self.userForm["rbound"]
        step = self.userForm["step"]
        points = []
        points.append(cur)

        while (cur < rbound):
            cur += step
            points.append(cur)

        self.functionPoints = points

    def generateFunctionTable(self):
        self.functionValues = []
        try:
            self.rpn = self.getRPN(self.userForm["func"])
        except RPNException:
                print("RPN expression can't be computed!")
                return

        for point in self.functionPoints:
            try:
                result = self.getFuncResByRPN(self.rpn, x=point).tolist()
            except RPNException:
                print("Function at point ", point, " can't be computed!")
                continue
            self.functionValues.append([point, result])

    def updateAll(self):
        self.table.update(self.functionValues)



    @staticmethod
    def popupError(error):
        errMessage = QMessageBox()
        errMessage.setWindowTitle("Error!")
        errMessage.setText(error)
        errMessage.exec_()

if __name__ == "__main__":
    rpn = RPN()

    unittest.main()

    app = QApplication(sys.argv)
    rpnApp = App()
    rpnApp.show()
    sys.exit(app.exec_())
