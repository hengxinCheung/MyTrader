literal = (
    "INTEGER",  # integer
    "FLOAT",  # float
    "STRING",  # string
    "BOOL",  # boolean, True or False
)

operator = (
    # arithmetic operator
    "PLUS",  # plus: +
    "MINUS",  # minus: -
    "TIMES",  # times: *
    "DIVIDE",  # divide: /
    # relation operator
    "EQ",  # equal: =
    "NE",  # not equal: <>
    "LT",  # less than: <
    "LE",  # less than and equal: <=
    "GT",  # greater than: >
    "GE",  # greater than and equal: >=
    # logical operator
    "AND",  # and: &&
    "OR",  # or: ||
    # assign operator
    "ASSIGN",  # assign: :=, :, ^^, ..
)

delimiter = (
    "COMMA",  # comma: ,
    "SEMI",  # semicolon: ;
    # "PERIOD",  # period：.
    # "COLON",    # colon：':'
    "LPAREN",  # left paren: (
    "RPAREN",  # right paren: )
    # "LBRACKET",  # left bracket: [
    # "RBRACKET",  # right bracket：]
    # "LBRACE",   # left brace: {
    # "RBRACE",   # right brace: }
)

reserved = (
    "IF",  # if
    "THEN",  # then
    "BEGIN",  # begin
    "END",  # end
    "VARIABLE",  # variable qualifier
    "AND",  # logical operator: &&
    "OR",  # logical operator: ||
)

# the tuple of token's name
tokens = literal + operator + delimiter + reserved + (
    "NEWLINE",  # newline
    "COMMENT",  # comment, the line start with '//'
    "ID",  # identifier, consist of letter, digit and underline but must be start with letter or underline
)
# remove duplication
tokens = tuple(set(tokens))

system_variable = (
    "O",  # open price
    "C",  # close price
    "H",  # highest price
    "L",  # lowest price
    "V",  # volume
)
