from PyQt5.QtWidgets import QApplication, QMessageBox
import unittest
from rpn import RPN, RPNBadFunction, RPNException, TestRPN, History
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
        self.historyValues = []

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
            self.popupError("no function was provided!")
            return
        if precision == "":
            self.popuperror("no function was provided!")
            return

        self.userForm["expression"] = func 

        try:
            self.userForm["lbound"] = float(leftBound)
            self.userForm["rbound"] = float(rightBound)
            self.userForm["step"] = float(step)
            self.userForm["precision"] = int(precision)
        except ValueError:
            self.popupError("Expected float number")
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

        cur = lbound
        points = [cur]

        while (True):
            cur += step

            if (cur > rbound or abs(cur - rbound) < 1e-3):
                cur = rbound
                points.append(round(cur, precision))
                break

            points.append(round(cur, precision))

        self.functionPoints = points

    def checkStep(self):
        if (self.userForm["step"] < 0.0):
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
        self.historyValues = []

        try:
            self.rpn, self.history = self.getRPN(self.userForm["expression"], x='x')
        except RPNBadFunction as e:
            self.popupError(str(e))
            return
        except Exception as e:
            self.popupError('Invalid expression')
            return    
        except RPNException:
            print("RPN expression can't be computed!")
            return

        for state in self.history.history:
            values = []
            for i, key in enumerate(state):
                if (key != 'stack'):
                    values.append(f'{state[key]}')
                else:
                    stackToStr = ''
                    for element in state[key]:
                        stackToStr += ' '
                        stackToStr += element
                    values.append(stackToStr)

            self.historyValues.append(values)

        self.exprLabel.setText("RPN expression: " + self.rpn)
        precision = self.userForm["precision"]

        for point in self.functionPoints:
            try:
                result = self.getFuncResByRPN(self.rpn, x=point)
            except RPNBadFunction as e:
                self.popupError(str(e))
                return
            except RPNException:
                print("Function at point", point, "can't be computed!")
                self.functionValues.append([f'{point}', "Выколото"])
                continue
            except ZeroDivisionError:
                print("Zero division at", point, "occured")
                self.functionValues.append([f'{point}', "Выколото"])
                continue
            self.functionValues.append([f'{point}', f'{round(result, precision)}'])

    def updateAll(self):
        self.funcTable.update(self.functionValues)
        self.historyTable.update(self.historyValues)

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
