from XETLast.ast import CompoundStatement, AssignStatement, BinopAexp, AndBexp, IfStatement, StringAexp, \
    IntAexp, NotBexp, VarAexp, RelopBexp, OrBexp, BoolAexp, FloatAexp, ConcatExpr, SliceExpr, LenExpr, ErrorExpr, \
    SplitExtractExpr, DateAexp
from XETLcore.combinators import Lazy, Phrase, Opt, Exp
from XETLparser.datatypes import keyword, date_field, num_float, num_int, string, boolean, variable, date
from XETLparser.precendence import precedence, any_operator_in_list
from XETLparser.search_operation import orm_count_if_exp, orm_directlink_exp, orm_sum_if_exp, orm_vlookup_exp



def parser_tree(tokens):
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

    return variable + keyword(':=') + (aexp() | if_stmt()) ^ process


def if_stmt():
    def process(parsed):
        (((((_, condition), _), true_stmt), false_parsed), _) = parsed
        if false_parsed:
            (_, false_stmt) = false_parsed
        else:
            false_stmt = None
        return IfStatement(condition, true_stmt, false_stmt)

    return keyword('IF') + keyword('(') + bexp() + keyword(';') + both() + Opt(
        keyword(';') + both()) + keyword(')') ^ process


def both():
    return aexp() | Lazy(if_stmt)


def slice_exp():
    def process(parsed):
        (((((((((_, _), var)), _), start), _), end), _)) = parsed
        return SliceExpr(var, start, end)

    return keyword('SLICE') + keyword('(') + \
           Lazy(aexp) + \
           keyword(',') + \
           (num_int ^ (lambda i: IntAexp(i))) + \
           keyword(',') + \
           (num_int ^ (lambda i: IntAexp(i))) + \
           keyword(')') ^ process


def concat_exp():
    def process(parsed):
        (((((((((_, _), string_1)), _), string_2), _), string_3), _)) = parsed
        return ConcatExpr(string_1, string_2, string_3)

    return keyword('CONCAT') + keyword('(') + \
           Lazy(aexp) + \
           keyword(',') + \
           Lazy(aexp) + \
           keyword(',') + \
           Lazy(aexp) + \
           keyword(')') ^ process


def split_extract_exp():
    def process(parsed):
        (((((((_, _), value), _), separator), _), segment), _) = parsed
        return SplitExtractExpr(value, separator, segment)

    return keyword('SPLIT') + keyword('(') + \
           Lazy(aexp) + \
           keyword(',') + \
           Lazy(aexp) + \
           keyword(',') + \
           Lazy(aexp) + \
           keyword(')') ^ process


def len_exp():
    def process(parsed):
        (((_, _), var), _) = parsed
        return LenExpr(var)

    return keyword('LEN') + keyword('(') + \
           Lazy(aexp) + \
           keyword(")") ^ process


def error_exp():
    def process(parsed):
        (((_, _), var), _) = parsed
        return ErrorExpr(var)

    return keyword('ERROR') + keyword('(') + \
           Lazy(aexp) + \
           keyword(")") ^ process


# Boolean expressions
def bexp():
    return precedence(bexp_term(), bexp_precedence_levels, process_logic)


def bexp_not():
    return keyword('NOT') + Lazy(bexp_term) ^ (lambda parsed: NotBexp(parsed[1]))


def bexp_term():
    return bexp_not() | bexp_relop() | bexp_group() | aexp_value()


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
    return aexp_value() | aexp_group() | \
           orm_sum_if_exp() | date_field() | \
           slice_exp() | concat_exp() | error_exp() | len_exp() | \
           orm_count_if_exp() | orm_vlookup_exp() | \
           orm_directlink_exp() | split_extract_exp()


def aexp_group():
    return keyword('(') + Lazy(aexp) + keyword(')') ^ process_group


def aexp_value():
    return (num_int ^ (lambda i: IntAexp(i))) | \
           (num_float ^ (lambda y: FloatAexp(y))) | \
           (variable ^ (lambda v: VarAexp(v))) | \
           (string ^ (lambda i: StringAexp(i))) | \
           (boolean ^ (lambda i: BoolAexp(i))) | \
           (date ^ (lambda i: DateAexp(i)))


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


# Operator keywords and precedence levels
aexp_precedence_levels = [
    ['*', '/'],
    ['+', '-'],
]

bexp_precedence_levels = [
    ['and'],
    ['or'],
]
