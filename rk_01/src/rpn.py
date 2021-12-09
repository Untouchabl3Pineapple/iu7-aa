import numexpr as ne


class RPN(object):
    def __init__(self):
        self.__stack = []
        self.__operations = {"(": 0, ")": 0, "+": 1, "-": 1, "*": 2, "/": 2, "%": 3, "\\": 3, "^": 4}

    def getRPN(self, input_func):
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

    @staticmethod
    def __checkParams(el, params):
        if el.isalpha():
            try:
                el = str(params[el])
            except:
                print("Not all parameters are specified")
                return
        return el

    def getFuncResByRPN(self, input_func, **params):
        for str_el in input_func:
            if str_el not in self.__operations and not str_el.isalpha() and not str_el.isdigit():
                print("Incorrect function")
                return
            elif str_el not in self.__operations:
                self.__stack.append(str_el)
            else:
                first_stack_el = str(self.__stack.pop())
                second_stack_el = str(self.__stack.pop())

                check = self.__checkParams(first_stack_el, params)
                if check: first_stack_el = str(check)
                else: return
                check = self.__checkParams(second_stack_el, params)
                if check: second_stack_el = str(check)
                else: return

                # custom signs
                if str_el == '^':
                    str_el = '**'
                elif str_el == '\\':
                    str_el = "//"

                res = ne.evaluate(second_stack_el + str_el + first_stack_el)
                self.__stack.append(res)

        return self.__stack.pop() # return last stack el = res


        


    

