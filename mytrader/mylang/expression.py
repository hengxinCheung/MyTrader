import time
from functools import wraps
from enum import Enum, unique, auto
from mytrader.mylang import builtins
from mytrader.mylang.error import EvalError


def eval_wrapper(func):
    @wraps(func)
    def wrapper(self, interpreter, env):
        interpreter.current_expr = self
        print("Executing expression: {}".format(self))
        return func(self, interpreter, env)
    return wrapper


@unique
class ExpressionType(Enum):
    """define the type of expression"""
    STRING = auto()
    NUMBER = auto()
    BOOL = auto()
    UNARY = auto()
    ARITHMETIC = auto()
    RELATION = auto()
    LOGICAL = auto()
    VARIABLE = auto()
    FUNCTION = auto()


class Expression(object):
    def __init__(self,
                 expression_type: ExpressionType,
                 operator: str,
                 operands: list,
                 start_line_number: int,
                 end_line_number: int,
                 start_position: int,
                 end_position: int):
        self.expression_type = expression_type
        self.operator = operator
        # operands must be a list, even if there is only one operand
        self.operands = operands
        # line number and position index of expression in source code
        self.start_line_number = start_line_number
        self.end_line_number = end_line_number
        self.start_position = start_position
        self.end_position = end_position

    @eval_wrapper
    def eval(self, interpreter, env):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


class String(Expression):
    def __init__(self, operands, start_line_number, end_line_number, start_position, end_position):
        super(String, self).__init__(ExpressionType.STRING, None, operands,
                                     start_line_number, end_line_number, start_position, end_position)

    @eval_wrapper
    def eval(self, interpreter, env):
        return self.operands[0]

    def __str__(self):
        return "\'{}\'".format(self.operands[0])


class Number(Expression):
    def __init__(self, operands, start_line_number, end_line_number, start_position, end_position):
        super(Number, self).__init__(ExpressionType.NUMBER, None, operands,
                                     start_line_number, end_line_number, start_position, end_position)

    @eval_wrapper
    def eval(self, interpreter, env):
        return self.operands[0]

    def __str__(self):
        return str(self.operands[0])


class Bool(Expression):
    def __init__(self, operands, start_line_number, end_line_number, start_position, end_position):
        super(Bool, self).__init__(ExpressionType.BOOL, None, operands,
                                   start_line_number, end_line_number, start_position, end_position)

    @eval_wrapper
    def eval(self, interpreter, env):
        return self.operands[0]

    def __str__(self):
        return str(self.operands[0])


class Unary(Expression):
    def __init__(self, operator, operands, start_line_number, end_line_number, start_position, end_position):
        super(Unary, self).__init__(ExpressionType.UNARY, operator, operands,
                                    start_line_number, end_line_number, start_position, end_position)

    @eval_wrapper
    def eval(self, interpreter, env):
        expr_value = self.operands[0].eval(interpreter, env)
        if not isinstance(expr_value, (int, float)):
            raise EvalError(self, "Bad operand type for unary: {!r}".format(type(expr_value)))
        if self.operator == "+":
            return expr_value
        elif self.operator == "-":
            return -expr_value

    def __str__(self):
        return "{}{}".format(self.operator, self.operands[0])


class Arithmetic(Expression):
    def __init__(self, operator, operands, start_line_number, end_line_number, start_position, end_position):
        super(Arithmetic, self).__init__(ExpressionType.ARITHMETIC, operator, operands,
                                         start_line_number, end_line_number, start_position, end_position)

    @eval_wrapper
    def eval(self, interpreter, env):
        # handle group (just one operand)
        if self.operator == "()":
            expr_value = self.operands[0].eval(interpreter, env)
            return expr_value
        # handle other situation with two operand
        left_value = self.operands[0].eval(interpreter, env)
        right_value = self.operands[1].eval(interpreter, env)
        if isinstance(left_value, (int, float)) and isinstance(right_value, (int, float)):
            if self.operator == "+":
                return left_value + right_value
            elif self.operator == "-":
                return left_value + right_value
            elif self.operator == "*":
                return left_value * right_value
            elif self.operator == "/":
                return left_value / right_value
        else:
            raise EvalError(self, "{!r} do not support between type {!r} and {!r}".format(
                self.operator, type(left_value), type(right_value)))

    def __str__(self):
        if self.operator == "()":
            return "({})".format(self.operands[0])
        else:
            return "{}{}{}".format(self.operands[0], self.operator, self.operands[1])


class Relation(Expression):
    def __init__(self, operator, operands, start_line_number, end_line_number, start_position, end_position):
        super(Relation, self).__init__(ExpressionType.RELATION, operator, operands,
                                       start_line_number, end_line_number, start_position, end_position)

    @eval_wrapper
    def eval(self, interpreter, env):
        left_value = self.operands[0].eval(interpreter, env)
        right_value = self.operands[1].eval(interpreter, env)
        if self.operator == "<":
            return left_value < right_value
        elif self.operator == "<=":
            return left_value <= right_value
        elif self.operator == ">":
            return left_value > right_value
        elif self.operator == ">=":
            return left_value >= right_value
        elif self.operator == "=":
            return left_value == right_value
        elif self.operator == "<>":
            return left_value != right_value

    def __str__(self):
        return "{}{}{}".format(self.operands[0], self.operator, self.operands[1])


class Logical(Expression):
    def __init__(self, operator, operands, start_line_number, end_line_number, start_position, end_position):
        super(Logical, self).__init__(ExpressionType.LOGICAL, operator, operands,
                                      start_line_number, end_line_number, start_position, end_position)

    @eval_wrapper
    def eval(self, interpreter, env):
        left_value = self.operands[0].eval(interpreter, env)
        right_value = self.operands[1].eval(interpreter, env)
        if self.operator == "&&" or self.operator == "AND":
            return left_value and right_value
        elif self.operator == "||" or self.operator == "OR":
            return left_value or right_value

    def __str__(self):
        return "{}{}{}".format(self.operands[0], self.operator, self.operands[1])


class Variable(Expression):
    def __init__(self, assign_statement, start_line_number, end_line_number, start_position, end_position):
        self.name = assign_statement.name
        self.value = assign_statement.value
        super(Variable, self).__init__(ExpressionType.VARIABLE, assign_statement.assign_symbol,
                                       assign_statement.expressions,
                                       start_line_number, end_line_number, start_position, end_position)

    def eval(self, interpreter, env):
        self.value = interpreter.variables[self.name].value
        return self.value

    def __str__(self):
        return self.name


class Function(Expression):
    def __init__(self, operator, operands, start_line_number, end_line_number, start_position, end_position):
        super(Function, self).__init__(ExpressionType.FUNCTION, operator, operands,
                                       start_line_number, end_line_number, start_position, end_position)

    @eval_wrapper
    def eval(self, interpreter, env):
        # all function must pose
        args = [env]
        # Get value of parameters
        for operand in self.operands:
            args.append(operand.eval(interpreter, env))
        # get a callable function according to the name of function
        func = getattr(builtins, self.operator)
        # call the function
        return func(*args)

    def __str__(self):
        return "{}({})".format(self.operator, ",".join([str(operand) for operand in self.operands]))