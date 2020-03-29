class LexError(Exception):
    def __init__(self, t):
        self.value = t.value[0]
        self.line_number = t.lineno
        self.position = t.lexpos
        self.error_msg = "[LexError] Line {}: Illegal character {!r}".format(
            self.line_number, self.value)
        super(LexError, self).__init__(self.error_msg)


class ParseError(Exception):
    def __init__(self, value, line_number, position, error_msg):
        self.value = value
        self.line_number = line_number
        self.position = position
        self.error_msg = "[ParserError] Line {}: {}".format(line_number, error_msg)
        super(ParseError, self).__init__(self.error_msg)


class GrammarError(ParseError):
    def __init__(self, p):
        value = ""
        line_number = 0
        position = -1
        if p:
            line_number = p.lineno
            position = p.lexpos
            value = p.value
            error_msg = "Invalid syntax occurs near {!r}".format(value)
        else:
            error_msg = "Invalid syntax at EOF"
        super(GrammarError, self).__init__(value, line_number, position, error_msg)


class UndefineError(ParseError):
    def __init__(self, value, line_number, position):
        error_msg = "Name {!r} not defined".format(value)
        super(UndefineError, self).__init__(value, line_number, position, error_msg)


class ArgumentError(ParseError):
    def __init__(self, value, line_number, position, correct_count, error_count):
        error_msg = "function {!r} takes {} positional argument but {} were given".format(
            value, correct_count, error_count)
        super(ArgumentError, self).__init__(value, line_number, position, error_msg)


class EvalError(Exception):
    def __init__(self, expr, msg: str):
        self.start_line_number = expr.start_line_number
        self.end_line_number = expr.end_line_number
        self.start_position = expr.start_position
        self.end_position = expr.end_position
        self.error_msg = "[EvalError] Line {}-{}: {} -> {}".format(
            self.start_line_number, self.end_line_number, expr, msg)
        super(EvalError, self).__init__(self.error_msg)
