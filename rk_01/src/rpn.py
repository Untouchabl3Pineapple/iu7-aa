import numexpr as ne


class RPN(object):
    def __init__(self):
        self.__stack = []
        self.__operations = {"(": 0, ")": 0, "+": 1, "-": 1, "*": 2, "/": 2, "%": 3, "\\": 3, "^": 4}

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

    def getRPN(self, input_func):
        input_func = self.__deleteSpaces(input_func)

        output_func = ""

        for str_el in input_func:
            if str_el not in self.__operations and not str_el.isalpha() and not str_el.isdigit():
                print("Incorrect function")
                return
            elif str_el not in self.__operations and (str_el.isalpha() or str_el.isdigit()):
                output_func += str_el
            elif str_el == "(":
                self.__stack.append(str_el)
            elif str_el == ")":
                top_el = self.__stack.pop()
                while top_el != "(":
                    output_func += top_el
                    top_el = self.__stack.pop()
            else:
                while (
                    len(self.__stack) != 0
                    and self.__operations[str_el] <= self.__operations[self.__stack[-1]]
                ):
                    output_func += self.__stack.pop()
                self.__stack.append(str_el)

        while len(self.__stack) != 0:
            output_func += self.__stack.pop()

        return output_func

    def getFuncResByRPN(self, input_func, **params):
        input_func = self.__deleteSpaces(input_func)
        subfunc = ""

        for str_el in input_func:
            if str_el not in self.__operations and not str_el.isalpha() and not str_el.isdigit():
                print("Incorrect function")
                return
            elif str_el not in self.__operations:
                if not str_el.isdigit(): # checking for a function call
                    subfunc += str_el
                    continue

                param = self.__getParam(subfunc, params)
                subfunc_res = self.__getSubFunctionRes(str_el, subfunc)

                if not param and not subfunc_res: 
                    return

                elif param:
                    self.__stack.append(subfunc) # param
                    self.__stack.append(str_el)
                    continue
                else:
                    self.__stack.append(subfunc_res)
                    subfunc = ""
            else:
                first_stack_el = str(self.__stack.pop())
                second_stack_el = str(self.__stack.pop())

                param = self.__getParam(first_stack_el, params)
                if param: first_stack_el = str(param)
                else: return
                param = self.__getParam(second_stack_el, params)
                if param: second_stack_el = str(param)
                else: return

                # custom signs
                if str_el == '^':
                    str_el = '**'
                elif str_el == '\\':
                    str_el = "//"

                res = ne.evaluate(second_stack_el + str_el + first_stack_el)
                self.__stack.append(res)

        return self.__stack.pop() # return last stack el = res


        


    

