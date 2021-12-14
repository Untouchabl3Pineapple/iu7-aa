from PyQt5.QtWidgets import QApplication, QMessageBox
import unittest
from rpn import RPN, RPNException, TestRPN
from gui import GUI
import sys


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


class App(RPN, GUI):
    def __init__(self):
        GUI.__init__(self)
        RPN.__init__(self)

        self.rel_tol = 1e-09
        self.functionPoints = []
        self.functionValues = []

    def processFunction(self):
        leftBound = self.leftBoundPrompt.text()
        rightBound = self.rightBoundPrompt.text()
        step = self.stepPrompt.text()
        func = self.functionPrompt.text()
        precision = self.precisionPrompt.text()

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
            self.popuperror("no function was provided!")
            return
        if precision == "":
            self.popuperror("no function was provided!")
            return

        self.userForm["expression"] = func 
        self.userForm["lbound"] = float(leftBound)
        self.userForm["rbound"] = float(rightBound)
        self.userForm["step"] = float(step)

        try:
            self.userForm["precision"] = int(precision)
        except ValueError:
            self.popupError("Precision is not int.")
            return

        if not self.checkStep():
            self.popupError("Step is not corrent value.")
            return

        if not self.checkPrecision():
            self.popupError("Precision is less than 1.")
            return

        self.findPointsInRange()

        self.generateFunctionTable()

        self.updateAll()

    def findPointsInRange(self):
        lbound = self.userForm["lbound"]
        rbound = self.userForm["rbound"]
        step = self.userForm["step"]
        precision = self.userForm["precision"]
        points = []

        if rbound > lbound:
            cur = lbound
            points.append(cur)
            while cur < rbound:
                cur += step
                points.append(round(cur, precision))
        else:
            cur = lbound
            points.append(cur)
            while cur > rbound:
                cur += step
                points.append(round(cur, precision))


        self.functionPoints = points

    def checkStep(self):
        if (self.userForm["lbound"] < self.userForm["rbound"] and self.userForm["step"] < 0.0):
            return False
        if (self.userForm["lbound"] > self.userForm["rbound"] and self.userForm["step"] > 0.0):
            return False
        if (isclose(self.userForm["step"], 0.0)):
                return False
        return True

    def checkPrecision(self):
        if (self.userForm["precision"] < 1):
            return False
        return True

    def generateFunctionTable(self):
        self.functionValues = []

        try:
            self.rpn = self.getRPN(self.userForm["expression"], x='x')
        except RPNException:
            print("RPN expression can't be computed!")
            return

        self.exprLabel.setText("RPN expression: " + self.rpn)
        precision = self.userForm["precision"]

        for point in self.functionPoints:
            try:
                result = self.getFuncResByRPN(self.rpn, x=point)
            except RPNException:
                print("Function at point", point, "can't be computed!")
                self.functionValues.append([f'{point}', "NaN"])
                continue
            except ZeroDivisionError:
                print("Zero division at", point, "occured")
                self.functionValues.append([f'{point}', "NaN"])
                continue
            self.functionValues.append([f'{point}', f'{round(result, precision)}'])

    def updateAll(self):
        self.table.update(self.functionValues)

    @staticmethod
    def popupError(error):
        errMessage = QMessageBox()
        errMessage.setWindowTitle("Error!")
        errMessage.setText(error)
        errMessage.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    rpnApp = App()
    rpnApp.show()
    sys.exit(app.exec_())
