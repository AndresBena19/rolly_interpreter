from XETLlexer.tokens import INT, FLOAT, STRING, BOOL, BOOL_VALUES, ID, DATE, RESERVED
from XETLcore.combinators import Tag, Reserved
from XETLast.ast import StringAexp, DateAexp, VarAexp

# Basic parsers
def keyword(kw):
    return Reserved(kw, RESERVED)


num_int = Tag(INT) ^ (lambda i: int(i))
num_float = Tag(FLOAT) ^ (lambda d: float(d))
string = Tag(STRING) ^ (lambda r: r.replace("'", '') if r[0] == "'" else r.replace('"', ''))
date = Tag(DATE) ^ (lambda r: r.replace("'", '') if r[0] == "'" else r.replace('"', ''))
boolean = Tag(BOOL) ^ (lambda r: BOOL_VALUES.get(r))
variable = Tag(ID)


def date_field():
    def process(parsed):
        from XETLast.ast import VarAexp, DateAexp, StringAexp

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
           ((date ^ (lambda i: DateAexp(i))) | (string ^ (lambda i: StringAexp(i))) | (variable ^ (lambda v: VarAexp(v)))) + \
           keyword(',') + \
           ((string ^ (lambda i: StringAexp(i))) | (variable ^ (lambda v: VarAexp(v)))) + \
           keyword(")") ^ process
