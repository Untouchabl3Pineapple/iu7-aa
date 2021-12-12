import numexpr as ne
import unittest
import re
import math

def trig_check(haystack:str):
    trig = ('sin', 'cos', 'tan', 'cot')
    for oper in trig:
        if haystack.startswith(oper):
            return oper

def cot(x):
    return 1 / math.tan(x)


class RPNException(Exception):
    pass


class RPN(object):
    def __init__(self):
        self.__stack = []
        self.__operations = {'sin':6, 'cos':6, 'tan':6, 'cot': 6, "(": 0, ")": 1, "+": 2, "-": 2, "*": 3, "/": 3, "%": 4, "\\": 3, "^": 5}

    @staticmethod
    def __deleteSpaces(input_func):
        return input_func.replace(" ", "")

    @staticmethod
    def __getParam(el, params):
        if el.isalpha():
            try:
                el = str(params[el])
            except:
                return
        return el

    @staticmethod
    def __getSubFunctionRes(val, subfunc):
        try:
            res = ne.evaluate(subfunc + '(' + val + ')')
        except:
            return
        return res

    def getRPN(self, input_func:str, **vars):
        input_func = self.__deleteSpaces(input_func)

        output_func = ""

        i = 0
        while i < len(input_func):
            str_el = input_func[i]

            if str_el == ' ':
                pass
            elif str_el not in self.__operations and not str_el.isalpha() and not str_el.isdigit():
                raise RPNException("Incorrect function was provided")
            
            elif str_el not in self.__operations and (str_el.isdigit()):
                while i < len(input_func) and input_func[i].isdigit():
                    output_func += input_func[i]
                    if i + 1 < len(input_func) and input_func[i + 1].isdigit():
                        i += 1
                    else:
                        break

                output_func += ' '
            
            elif vars.get(str_el) is not None:
                output_func += str_el
                output_func += ' '

            elif str_el == "(":
                self.__stack.append(str_el)

            elif str_el == ")":
                top_el = self.__stack.pop()
                while top_el != "(":
                    output_func += top_el
                    output_func += ' '
                    top_el = self.__stack.pop()
            else:
                oper = str_el
                
                if str_el in ('s', 'c', 't'):
                    oper = trig_check(input_func[i:])
                    i += len(oper) - 1
                

                while (
                        len(self.__stack) != 0
                        and self.__operations[oper] <= self.__operations[self.__stack[-1]]
                        ):
                    output_func += self.__stack.pop()
                    output_func += ' '

                self.__stack.append(oper)
            
            i += 1

        while len(self.__stack) != 0:
            output_func += self.__stack.pop()
            output_func += ' '

        return output_func
    
    def getFuncResByRPN(self, func:str, **params):
        func = func.split()

        unary = {'sin': math.sin, 'cos': math.cos, 'tan' : math.tan, 'cot': lambda x : cot(x)}
        binary = {'+'  : lambda x, y: x +  y,
                  '-'  : lambda x, y: x -  y,
                  '*'  : lambda x, y: x *  y,
                  '/'  : lambda x, y: x /  y,
                  '\\' : lambda x, y: x // y,
                  '^'  : lambda x, y: x ** y,
                  '%'  : lambda x, y: x % y}

        operand_queue = []

        res = 0

        for i in func:
            if i in self.__operations:
                if i in unary:
                    oper = float(operand_queue.pop())
                    res = unary[i](oper)
                else:
                    r = float(operand_queue.pop())
                    l = float(operand_queue.pop())

                    res = binary[i](l, r)
                operand_queue.append(res)
            elif i.isdigit():
                operand_queue.append(i)
            else:
                try:
                    operand_queue.append(params[i])
                except KeyError:
                    raise RPNException("Incorrect function was provided")
        
        return res

class TestRPN(unittest.TestCase, RPN):

    def test_arithmetics(self):
        rpn = RPN()
        expr = rpn.getRPN("x - 4", x=0)
        result = rpn.getFuncResByRPN(expr, x=10)
        self.assertEqual(result, 6)

    def test_sine(self):
        rpn = RPN()
        expr = rpn.getRPN("sin(x)", x=0)
        result = rpn.getFuncResByRPN(expr, x=10)
        self.assertEqual(result, -0.54402111)

    def test_cosine(self):
        rpn = RPN()
        expr = rpn.getRPN("cos(x)", x=0)
        result = rpn.getFuncResByRPN(expr, x=10)
        self.assertEqual(result, -0.83907153)

    def test_exponent(self):
        rpn = RPN()
        expr = rpn.getRPN("x^2", x=0)
        result = rpn.getFuncResByRPN(expr, x=10)
        self.assertEqual(result, 100)

    def test_division(self):
        rpn = RPN()
        expr = rpn.getRPN("x / 2", x=0)
        result = rpn.getFuncResByRPN(expr, x=10)
        self.assertEqual(result, 5)

    def test_whole_division(self):
        rpn = RPN()
        expr = rpn.getRPN("x \\ 2", x=0)
        result = rpn.getFuncResByRPN(expr, x=10)
        self.assertEqual(result, 5)

    def test_modulo(self):
        rpn = RPN()
        expr = rpn.getRPN("x % 3", x=0)
        result = rpn.getFuncResByRPN(expr, x=5)
        self.assertEqual(result, 2)
