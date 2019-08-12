from collections import deque
import sys
from typing import FrozenSet, List, Dict, Deque, Generator

from utils import Stack

symbols: FrozenSet[str] = frozenset(["^", "%", "+", "-", "*", "/", "(", ")"])
priority: Dict[str, int] = {"(": 0, "^": 3, "%": 3, "*": 2, "/": 2, "+": 1, "-": 1}
reserved_set: FrozenSet[str] = frozenset(["exit", "history"])


class SymbolError(Exception):
    pass


class ExitError(Exception):
    pass


def welcome() -> None:
    sys.stdout.write("Welcome to cal v0.1\nauthor:Python高效编程\n\n")


def read(prompt="cal> ") -> str:
    sys.stdout.write(prompt)
    sys.stdout.flush()
    iput: str = sys.stdin.readline()
    return iput


def tokenize(expression: str) -> Generator[str, None, None]:
    for symbol in symbols:
        # 替换字符串
        expression = expression.replace(symbol, f" {symbol} ")
    # 分割字符串
    seq: List[str] = expression.split()
    for i, item in enumerate(expression.split()):
        if item == "-":
            # 两种情况下，当前符号设置为 ""
            # 下一个符号设置为负数
            if i - 1 < 0 or seq[i - 1] == "(":
                seq[i] = ""
                seq[i + 1] = f"-{seq[i + 1]}"
        # 若字符串不为空，打印字符串
        if seq[i]:
            yield seq[i]


def compare_priority(first: str, second: str) -> bool:
    f_priority: int = priority[first]
    s_priority: int = priority[second]
    return f_priority <= s_priority


def is_float(num: str) -> bool:
    try:
        float(num)
    except ValueError:
        return False
    else:
        return True


def parse_infix(expression: str) -> List[str]:
    stack: Stack[str] = Stack()
    result: List[str] = []
    for expr in tokenize(expression):
        if not is_float(expr) and expr not in symbols:
            raise SymbolError()

        if is_float(expr):
            result.append(expr)

        elif expr == ")":
            while stack.top != "(":
                result.append(stack.pop())
            stack.pop()

        elif expr == "(":
            stack.push(expr)

        elif stack.top and compare_priority(expr, stack.top):
            result.append(stack.pop())
            while stack.top and compare_priority(expr, stack.top):
                result.append(stack.pop())
            stack.push(expr)
        else:
            stack.push(expr)

    while stack:
        result.append(stack.pop())
    return result


def parse_sufix(expression: List[str]) -> float:
    stack: Stack[str] = Stack()
    result: float = 0.0
    for expr in expression:
        if is_float(expr):
            stack.push(expr)
        else:
            elem1: str = stack.pop()
            elem2: str = stack.pop()
            result = evaluate(expr, float(elem2), float(elem1))
            stack.push(str(result))
    if stack:
        result = float(stack.pop())
    return result


def evaluate(symbol: str, num1: float, num2: float) -> float:
    if symbol == "+":
        return num1 + num2
    elif symbol == "-":
        return num1 - num2
    elif symbol == "*":
        return num1 * num2
    elif symbol == "/":
        try:
            return num1 / num2
        except ZeroDivisionError:
            print("除数不可以为零")


def parse(sentence: str) -> float:
    expr_infix: List[str] = parse_infix(sentence)
    value: float = parse_sufix(expr_infix)
    return value


def reversed_op(operator: str, history: Deque[str]) -> None:
    if operator == "exit":
        raise ExitError()
    elif operator == "history":
        sys.stdout.write("*" * 30 + "\n")
        for item in history:
            sys.stdout.write(f"{item}\n")
        sys.stdout.write("*" * 30 + "\n")


def loop() -> None:
    welcome()
    history: Deque[str] = deque(maxlen=5)
    running: bool = True
    while running:
        result: str = read().strip()
        if result in reserved_set:
            try:
                reversed_op(result, history)
            except ExitError:
                running = False
            continue

        try:
            eval_value: float = parse(result)
        except SymbolError:
            sys.stdout.write("表达式不合法请重新输入\n")
        except OverflowError:
            sys.stdout.write("数值过大请重新输入\n")
        except:
            sys.stdout.write("请重新输入\n")
        else:
            sys.stdout.write(f"{eval_value}\n")
            history.append(result)
    sys.stdout.write("see you later!")


def main():
    loop()


if __name__ == "__main__":
    main()