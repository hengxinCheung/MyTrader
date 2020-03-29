from functools import wraps
from enum import Enum, unique, auto
from mytrader.mylang.error import EvalError


def eval_wrapper(func):
    @wraps(func)
    def wrapper(self, interpreter, env):
        interpreter.current_statement = self
        print("Executing statement: {}".format(self))
        return func(self, interpreter, env)
    return wrapper


@unique
class StatementType(Enum):
    """define the type of statement"""
    NORMAL = auto()
    ASSIGN = auto()
    CONDITIONAL = auto()
    IF = auto()


class Statement(object):
    def __init__(self, statement_type: StatementType,
                 start_line_number, end_line_number, start_position, end_position):
        self.statement_type = statement_type
        self.start_line_number = start_line_number
        self.end_line_number = end_line_number
        self.start_position = start_position
        self.end_position = end_position
        # the value of statement
        self.value = None

    @eval_wrapper
    def eval(self, interpreter, env):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


class NormalStatement(Statement):
    def __init__(self, expression, start_line_number, end_line_number, start_position, end_position):
        super(NormalStatement, self).__init__(StatementType.NORMAL,
                                              start_line_number, end_line_number, start_position, end_position)
        self.expression = expression

    @eval_wrapper
    def eval(self, interpreter, env):
        self.value = self.expression.eval(interpreter, env)
        return self.value

    def __str__(self):
        return "{};".format(str(self.expression))


class AssignStatement(Statement):
    def __init__(self, name, assign_symbol, expression,
                 start_line_number, end_line_number, start_position, end_position):
        super(AssignStatement, self).__init__(StatementType.ASSIGN,
                                              start_line_number, end_line_number, start_position, end_position)
        self.name = name
        self.assign_symbol = assign_symbol
        self.expression = expression

    @eval_wrapper
    def eval(self, interpreter, env):
        # add self to variable table
        interpreter.variables[self.name] = self
        # eval the expression and get the value of variable
        self.value = self.expression.eval(interpreter, env)

    def __str__(self):
        return "{} {} {};".format(self.name, self.assign_symbol, self.expression[0])


class ConditionalStatement(Statement):
    def __init__(self, condition, expression, start_line_number, end_line_number, start_position, end_position):
        super(ConditionalStatement, self).__init__(StatementType.CONDITIONAL,
                                                   start_line_number, end_line_number,
                                                   start_position, end_position)
        self.condition = condition
        self.expression = expression

    @eval_wrapper
    def eval(self, interpreter, env):
        condition_value = self.condition.eval(interpreter, env)
        if condition_value is True or condition_value > 0:
            self.value = self.expression.eval(interpreter, env)

    def __str__(self):
        return "{}, {};".format(self.condition, self.expression)


class IfStatement(Statement):
    def __init__(self, condition, statements, start_line_number, end_line_number, start_position, end_position):
        super(IfStatement, self).__init__(StatementType.IF,
                                          start_line_number, end_line_number, start_position, end_position)
        self.condition = condition
        self.statements = statements

    @eval_wrapper
    def eval(self, interpreter, env):
        condition_value = self.condition.eval(interpreter, env)
        if condition_value is True or condition_value > 0:
            for statement in self.statements:
                statement.eval(interpreter, env)

    def __str__(self):
        return "IF {} THEN\nBEGIN\n{}\nEND".format(
            self.condition, "\n".join([str(statement) for statement in self.statements]))
