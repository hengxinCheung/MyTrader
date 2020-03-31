import sys
from ply import yacc
from ply.lex import LexToken
from ply.yacc import YaccProduction, LRParser
from mytrader.mylang.constants import tokens, system_variable
from mytrader.mylang.lex import create_lexer
from mytrader.mylang import builtins
from mytrader.mylang.expression import Unary, Number, String, Bool, Arithmetic, Relation, Logical, Variable, Function
from mytrader.mylang.statement import NormalStatement, AssignStatement, ConditionalStatement, IfStatement
from mytrader.mylang.error import ParseError, UndefineError, GrammarError, ArgumentError

# define the precedence of operator
precedence = (
    ('left', 'AND', 'OR'),
    ('left', 'EQ', 'NE', 'LT', 'GT', 'LE', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UPLUS', 'UMINUS')
)


def p_statement(p: YaccProduction):
    """statements : statement
                  | statements statement"""
    if len(p) == 2:
        p[0] = []
        p[0].append(p[1])
    elif len(p) == 3:
        p[0] = p[1]
        p[0].append(p[2])


def p_statement_normal(p: YaccProduction):
    """statement : expr SEMI"""
    p[0] = NormalStatement(p[1], p[1].start_line_number, p.lineno(2), p[1].start_position, p.lexpos(2))


def p_statement_conditional(p: YaccProduction):
    """statement : expr COMMA expr SEMI"""
    p[0] = ConditionalStatement(p[1], p[3], p[1].start_line_number, p.lineno(4), p[1].start_position, p.lexpos(4))


def p_statement_assign(p: YaccProduction):
    """statement : ID ASSIGN expr SEMI"""
    # judge whether id is same as system variables
    if p[1] in system_variable:
        raise ParseError(p[1], p.lineno(1), p.lexpos(1), "name of variable can not same as system variables")
    # register variable in parser, and it will help us detect undefine error early
    variables: dict = p.parser.variables
    p[0] = AssignStatement(p[1], p[2], p[3], p.lineno(1), p.lineno(4), p.lexpos(1), p.lexpos(4))
    variables[p[1]] = p[0]


def p_statement_if(p: YaccProduction):
    """statement : IF expr THEN BEGIN statements END"""
    p[0] = IfStatement(p[2], p[5], p.lineno(1), p.lineno(6), p.lexpos(1), p.lexpos(6)+len(p[6])-1)


def p_expr_number(p: YaccProduction):
    """expr : INTEGER
            | FLOAT
            | INTEGER FLOAT"""
    if len(p) == 2:
        p[0] = Number([p[1]], p.lineno(1), p.lineno(1), p.lexpos(1), p.lexpos(1) + len(str(p[1])) - 1)
    elif len(p) == 3:
        p[0] = Number([p[1] + p[2]], p.lineno(1), p.lineno(2), p.lexpos(1), p.lexpos(2) + len(str(p[2])))


def p_expr_string(p: YaccProduction):
    """expr : STRING"""
    p[0] = String([p[1]], p.lineno(1), p.lineno(1), p.lexpos(1), p.lexpos(1) + len(p[1]) - 1)


def p_expr_bool(p: YaccProduction):
    """expr : BOOL"""
    p[0] = Bool([p[1]], p.lineno(1), p.lineno(1), p.lexpos(1), p.lexpos(1) + len(str(p[1])))


def p_expr_unary(p: YaccProduction):
    """expr : MINUS expr %prec UMINUS
            | PLUS expr %prec UPLUS"""
    p[0] = Unary(p[1], [p[2]], p.lineno(1), p[2].end_line_number, p.lexpos(1), p[2].end_position)


def p_expr_arithmetic(p: YaccProduction):
    """expr : LPAREN expr RPAREN
            | expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr"""
    if p[1] == "(" and p[3] == ")":
        p[0] = Arithmetic("()", [p[2]], p.lineno(1), p.lineno(3), p.lexpos(1), p.lexpos(3))
    else:
        p[0] = Arithmetic(p[2], [p[1], p[3]],
                          p[1].start_line_number, p[3].end_line_number, p[1].start_position, p[3].end_position)


def p_expr_relation(p: YaccProduction):
    """expr : expr EQ expr
            | expr NE expr
            | expr LT expr
            | expr LE expr
            | expr GT expr
            | expr GE expr
            | expr LT EQ expr
            | expr GT EQ expr"""
    if len(p) == 4:
        p[0] = Relation(p[2], [p[1], p[3]],
                        p[1].start_line_number, p[3].end_line_number, p[1].start_position, p[3].end_position)
    elif len(p) == 5:
        p[0] = Relation(p[2] + p[3], [p[1], p[4]],
                        p[1].start_line_number, p[4].end_line_number, p[1].start_position, p[4].end_position)


def p_expr_logical(p: YaccProduction):
    """expr : expr AND expr
            | expr OR expr"""
    p[0] = Logical(p[2], [p[1], p[3]],
                   p[1].start_line_number, p[3].end_line_number, p[1].start_position, p[3].end_position)


def p_expr_variable(p: YaccProduction):
    """expr : ID"""
    # Get the the table of variable from parser
    variables: dict = p.parser.variables
    # If the variable has not been defined, raise error
    if p[1] not in variables.keys() or p[1] not in system_variable:
        raise UndefineError(p[1], p.lineno(1), p.lexpos(1))
    # If the variable has been defined, get variable from table
    p[0] = Variable(variables.get(p[1]), p.lineno(1), p.lineno(1), p.lexpos(1), p.lexpos(1) + len(p[1]) - 1)


def p_args(p: YaccProduction):
    """args : args COMMA expr
            | expr"""
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    elif len(p) == 2:
        p[0] = []
        p[0].append(p[1])


def p_expr_function(p: YaccProduction):
    """expr : ID LPAREN RPAREN
            | ID LPAREN args RPAREN"""
    # Judge whether the function has been defined
    if p[1] not in dir(builtins):
        raise UndefineError(p[1], p.lineno(1), p.lexpos(1))
    # Judge the count of arguments
    if len(p) == 4:
        input_args_count = 0
    elif len(p) == 5:
        print(p[3])
        input_args_count = len(p[3])
    func = getattr(builtins, p[1])
    args_count = func.__code__.co_argcount
    # why minus 1: because builtin function will be injected argument of 'env' at the first position
    if input_args_count != args_count - 1:
        raise ArgumentError(p[1], p.lineno(1), p.lexpos(1), args_count-1, input_args_count)
    if len(p) == 4:
        p[0] = Function(p[1], [], p.lineno(1), p.lineno(3), p.lexpos(1), p.lexpos(3))
    elif len(p) == 5:
        p[0] = Function(p[1], p[3], p.lineno(1), p.lineno(4), p.lexpos(1), p.lexpos(4))


def p_error(p: (LexToken, None)):
    raise GrammarError(p)


def create_parser():
    parser: LRParser = yacc.yacc(debug=0)
    return parser
