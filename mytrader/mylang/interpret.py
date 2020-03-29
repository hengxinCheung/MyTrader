from mytrader.mylang.lex import create_lexer
from mytrader.mylang.parse import create_parser
from mytrader.mylang.env import Environment, RealEnvironment


class Interpreter(object):
    def __init__(self, env: Environment):
        # execute environment
        self.env = env

        # the table of variable, {name of variable: assign statement}
        self.variables = dict()
        # the table of function, {name of function: function definition}
        self.functions = dict()
        # the list of statement
        self.statements = list()

        self.code = ""
        self.lexer = None
        self.parser = None

        self.current_expr = None
        self.current_statement = None

    def compile(self, code):
        # save the source code
        self.code = code
        # create the lexer and parser
        self.lexer = create_lexer()
        self.parser = create_parser()
        # add attribute 'variables' with type of set for parser
        setattr(self.parser, "variables", dict())
        # compile the code and get the statements
        self.statements = self.parser.parse(input=code, lexer=self.lexer)

        return self.statements

    def execute(self):
        for statement in self.statements:
            statement.eval(self, self.env)
