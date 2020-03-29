import sys
from mytrader.mylang import constants
from mytrader.mylang.constants import tokens
from ply import lex
from ply.lex import Lexer, LexToken
from mytrader.mylang.error import LexError


def str2bool(s: str):
    """transform str to boolean"""
    s = s.upper()
    if s == "TRUE":
        return True
    elif s == "FALSE":
        return False
    else:
        raise ValueError("can't transform {!r} to bool".format(s))


# ------------------------------------------------------------------
# define the regular expression of token and decide how to handle
# ------------------------------------------------------------------

# ignore the whitespace
t_ignore = "[ \f\t]"
# ignore the comment
t_ignore_COMMENT = r"//.*"
# define the operator
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_EQ = r"="
t_NE = r"<>"
t_LT = r"<"
t_LE = r"<="
t_GT = r">"
t_GE = r">="
t_AND = r"&&"
t_OR = r"OR"
t_ASSIGN = r":=|:|\^\^|\.\."
# define the delimiter
t_COMMA = r"\,"
t_SEMI = r";"
t_LPAREN = r"\("
t_RPAREN = r"\)"


def t_ignore_NEWLINE(t: LexToken):
    r"""\r?\n"""
    t.lexer.lineno += 1


def t_ID(t: LexToken):
    r"""[_a-zA-Z][_a-zA-Z0-9]*"""
    # upper the token because MyLang is case insensitive
    t.value = t.value.upper()
    # handle special condition
    if t.value == "TRUE" or t.value == "FALSE":
        t.type = "BOOL"
        t.value = str2bool(t.value)
    elif t.value in constants.reserved:
        t.type = t.value
    return t


def t_INTEGER(t: LexToken):
    r"""([1-9][0-9]*)|0"""
    t.value = int(t.value)
    return t


def t_FLOAT(t: LexToken):
    r"""\.[0-9]+"""
    t.value = float(t.value)
    return t


def t_STRING(t: LexToken):
    r"""(\'.*?\')|(\".*?\")"""
    # remove the quote
    t.value = t.value[1:-1]
    return t


# define how to handle error
def t_error(t: LexToken):
    raise LexError(t)


# create the Lexical Analyzer
def create_lexer(debug=False, optimize=False, lextab='lextab', outputdir=None):
    lexer: Lexer = lex.lex(module=None,
                           optimize=optimize,
                           debug=debug,
                           lextab=lextab,
                           outputdir=outputdir)
    return lexer


def tokenizer(s: str, lexer: Lexer):
    """tokenizer the code, and return the list of token"""
    result = []
    lexer.input(s)
    while True:
        token = lexer.token()
        # no more input
        if not token:
            break
        result.append(token)
    return result
