from rpn import RPN


if __name__ == "__main__":
    rpn = RPN()

    res = rpn.getRPN("3*2^3")
    print(res)

    print(rpn.getFuncResByRPN(res, x=5))
