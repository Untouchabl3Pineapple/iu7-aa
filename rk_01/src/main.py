from rpn import RPN


if __name__ == "__main__":
    rpn = RPN()

    res = rpn.getRPN("sin(3) + 422 + 3   %3 / 2")
    print(res)

    print(rpn.getFuncResByRPN(res, x=5))
