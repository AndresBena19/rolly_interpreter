from lexer import *
from combinators import *
from ast import *



# Basic parsers
def keyword(kw):
    return Reserved(kw, RESERVED)


num_int = Tag(INT) ^ (lambda i: int(i))
num_float = Tag(FLOAT) ^ (lambda d: float(d))
string = Tag(STRING) ^ (lambda r: r.replace("'", '') if r[0] == "'" else r.replace('"', ''))
date = Tag(DATE) ^ (lambda r: r.replace("'", '') if r[0] == "'" else r.replace('"', ''))
boolean = Tag(BOOL) ^ (lambda r: BOOL_VALUES.get(r))
id = Tag(ID)


# Top level parser
def rolly_parser(tokens):
    ast = parser()
    return ast(tokens, 0)


def parser():
    return Phrase(stmt_list())


# Statements
def stmt_list():
    separator = keyword(':') ^ (lambda x: lambda l, r: CompoundStatement(l, r))
    return Exp(stmt(), separator)


def stmt():
    return assign_stmt() | if_stmt()


def assign_stmt():
    def process(parsed):
        ((name, _), exp) = parsed
        return AssignStatement(name, exp)

    return id + keyword(':=') + (aexp() | bexp()) ^ process


def if_stmt():
    def process(parsed):
        (((((_, condition), _), true_stmt), false_parsed), _) = parsed
        if false_parsed:
            (_, false_stmt) = false_parsed
        else:
            false_stmt = None
        return IfStatement(condition, true_stmt, false_stmt)

    return keyword('if') + keyword('(') + bexp() + keyword(';') + Lazy(stmt_list) + Opt(
        keyword(';') + Lazy(stmt_list)) + keyword(')') ^ process


#Dates
def date_field():
    def process(parsed):
        (((((_, _), date), _), format), _) = parsed

        if isinstance(date, VarAexp):
            date = date.name
        elif isinstance(date, StringAexp):
            date = date.b
        elif isinstance(date, DateAexp):
            date = date.i

        if isinstance(format, VarAexp):
            format = format.name
        elif isinstance(format, StringAexp):
            format = format.b

        return DateAexp(date, format)

    return keyword('date') + keyword('(') + \
           ((date ^ (lambda i: DateAexp(i))) | (string ^ (lambda i: StringAexp(i)))|(id ^ (lambda v: VarAexp(v)))) + \
           keyword(',') + \
           ((string ^ (lambda i: StringAexp(i))) | (id ^ (lambda v: VarAexp(v)))) + \
           keyword(")") ^ process


# Boolean expressions
def bexp():
    return precedence(bexp_term(), bexp_precedence_levels, process_logic)


def bexp_not():
    return keyword('not') + Lazy(bexp_term) ^ (lambda parsed: NotBexp(parsed[1]))


def bexp_term():
    return bexp_not() | bexp_relop() | bexp_group() | (boolean) ^ (lambda i: BoolAexp(i)) | (id ^ (lambda v: VarAexp(v)))


def bexp_relop():
    relops = ['<', '<=', '>', '>=', '=', '!=']
    return aexp() + any_operator_in_list(relops) + aexp() ^ process_relop


def bexp_group():
    return keyword('(') + Lazy(bexp) + keyword(')') ^ process_group


# Arithmetic expressions
def aexp():
    return precedence(aexp_term(),
                      aexp_precedence_levels,
                      process_binop)


def aexp_term():
    return aexp_value() | aexp_group() | date_field()


def aexp_group():
    return keyword('(') + Lazy(aexp) + keyword(')') ^ process_group


def aexp_value():
    return (num_int ^ (lambda i: IntAexp(i))) | \
           (num_float ^ (lambda y: FloatAexp(y))) | \
           (id ^ (lambda v: VarAexp(v))) | \
           (string ^ (lambda i: StringAexp(i))) | \
           (boolean) ^ (lambda i: BoolAexp(i))


# An IMP-specific combinator for binary operator expressions (aexp and bexp)
def precedence(value_parser, precedence_levels, combine):
    def op_parser(precedence_level):
        return any_operator_in_list(precedence_level) ^ combine

    parser = value_parser * op_parser(precedence_levels[0])
    for precedence_level in precedence_levels[1:]:
        parser = parser * op_parser(precedence_level)
    return parser


# Miscellaneous functions for binary and relational operators
def process_binop(op):
    return lambda l, r: BinopAexp(op, l, r)


def process_relop(parsed):
    ((left, op), right) = parsed
    return RelopBexp(op, left, right)


def process_logic(op):
    if op == 'and':
        return lambda l, r: AndBexp(l, r)
    elif op == 'or':
        return lambda l, r: OrBexp(l, r)
    else:
        raise RuntimeError('unknown logic operator: ' + op)


def process_group(parsed):
    ((_, p), _) = parsed
    return p


def any_operator_in_list(ops):
    op_parsers = [keyword(op) for op in ops]
    parser = reduce(lambda l, r: l | r, op_parsers)
    return parser


# Operator keywords and precedence levels
aexp_precedence_levels = [
    ['*', '/'],
    ['+', '-'],
]

bexp_precedence_levels = [
    ['and'],
    ['or'],
]
