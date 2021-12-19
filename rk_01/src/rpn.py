import numexpr as ne
import unittest
import re
import math

def trig_check(haystack:str):
    trig = ('sin', 'cos', 'tan', 'cot')
    for oper in trig:
        if haystack.startswith(oper):
            return oper

def is_numeric(str):
    try:
        float(str)
        return True
    except:
        return False

def cot(x):
    return 1 / math.tan(x)


class RPNException(Exception):
    pass

class RPNBadFunction(Exception):
    pass

class History(object):
    def __init__(self):
        self.history = []

    def capture(self, index, symbol, array, stack):
        self.history.append({ 'index': index, 'symbol': symbol, 'array': array, 'stack': stack.copy() })

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
        # input_func = self.__deleteSpaces(input_func)


        output_func = ""
        history = History()

        braces = 0

        i = 0
        while i < len(input_func):
            str_el = input_func[i]


            if str_el == ' ':
                pass
            elif str_el not in self.__operations and not str_el.isalpha() and not str_el.isdigit() and not str_el == '.':
                raise RPNBadFunction("Incorrect function was provided")
            
            elif str_el not in self.__operations and (str_el.isdigit()):
                dot = False
                if i > 0 and input_func[i - 1] == '-':
                    output_func += '-'
                    history.capture(i, str_el, output_func, self.__stack)
                while i < len(input_func) and (input_func[i].isdigit() or input_func[i] == '.'):
                    if dot and input_func[i] == '.':
                        raise RPNBadFunction('Incorrect float number')
                    
                    dot = dot or input_func[i] == '.'

                    output_func += input_func[i]
                    history.capture(i, input_func[i], output_func, self.__stack)
                    if i + 1 < len(input_func) and (input_func[i + 1].isdigit() or input_func[i + 1] == '.'):
                        i += 1
                    else:
                        break

                output_func += ' '
            
            elif vars.get(str_el) is not None:
                if i > 0 and input_func[i - 1] == '-':
                    output_func += '-' 
                    history.capture(i, str_el, output_func, self.__stack)
                output_func += str_el
                output_func += ' '
                history.capture(i, str_el, output_func, self.__stack)

            elif str_el == "(":
                self.__stack.append(str_el)
                history.capture(i, str_el, output_func, self.__stack)
                braces += 1

            elif str_el == ")":
                if braces == 0:
                    raise RPNBadFunction('Bad braces')
                braces -= 1
                history.capture(i, str_el, output_func, self.__stack)
                top_el = self.__stack.pop()
                while top_el != "(":
                    output_func += top_el
                    output_func += ' '
                    history.capture(i, str_el, output_func, self.__stack)
                    top_el = self.__stack.pop()
                    history.capture(i, str_el, output_func, self.__stack)
            else:
                oper = str_el
                
                if str_el in ('s', 'c', 't'):
                    oper = trig_check(input_func[i:])
                    i += len(oper) - 1
                    history.capture(i, str_el, output_func, self.__stack)
                
                if str_el == '-' and (is_numeric(input_func[i + 1]) or input_func[i + 1].isalpha()):
                    pass
                else:
                    while (
                            len(self.__stack) != 0
                            and self.__operations[oper] <= self.__operations[self.__stack[-1]]
                            ):
                        history.capture(i, str_el, output_func, self.__stack)
                        output_func += self.__stack.pop()
                        output_func += ' '
                        history.capture(i, str_el, output_func, self.__stack)

                    self.__stack.append(oper)
                    history.capture(i, str_el, output_func, self.__stack)
            
            i += 1
            history.capture(i, str_el, output_func, self.__stack)

        while len(self.__stack) != 0:
            history.capture(i, str_el, output_func, self.__stack)
            output_func += self.__stack.pop()
            output_func += ' '
            history.capture(i, str_el, output_func, self.__stack)

        return output_func, history
    
    def getFuncResByRPN(self, func:str, **params):
        func = func.split()

        unary = {'sin': math.sin, 'cos': math.cos, 'tan' : math.tan, 'cot': lambda x : cot(x)}
        binary = {'+'  : lambda x, y: x +  y,
                  '-'  : lambda x, y: x -  y,
                  '*'  : lambda x, y: x *  y,
                  '/'  : lambda x, y: x /  y,
                  '\\' : lambda x, y: x // y,
                  '^'  : lambda x, y: x ** y,
                  '%'  : lambda x, y: x % y
                }

        operand_queue = []

        res = 0

        for i in func:
            if i in self.__operations:
                if i in unary:
                    if len(operand_queue) < 1:
                        raise RPNBadFunction('Expected operand')
                    oper = float(operand_queue.pop())
                    res = unary[i](oper)
                else:
                    if len(operand_queue) < 2:
                        raise RPNBadFunction('Expected operand')
                    r = operand_queue.pop()
                    l = operand_queue.pop()

                    res = binary[i](l, r)
                operand_queue.append(res)
            elif is_numeric(i):
                operand_queue.append(float(i))
            else:
                try:
                    if i[0] == '-':
                        i = i[1:]
                        operand_queue.append(-params[i])
                    else:
                        operand_queue.append(params[i])
                except KeyError:
                    raise RPNBadFunction("Incorrect expression.")
        if len(operand_queue) > 1:
            print(operand_queue)
            raise RPNBadFunction('Expected operator')
        if len(operand_queue) > 0:
            res = operand_queue.pop()
        
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
 
