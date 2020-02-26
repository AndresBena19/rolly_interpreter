from XETLparser.datatypes import keyword, num_int, variable
from XETLast.ast import IntAexp, VarAexp
from XETLast.search_operation import SumIfExpr, VlookupExpr, DirectLinkExpr, CountIfExpr
from XETLcore.combinators import Lazy


def option():
    from XETLparser.operations import aexp
    return Lazy(aexp)


def orm_sum_if_exp():
    def process(parsed):
        (((((((((((((((((((_, _), model), _), manager), _), signo), _), var_name), _), var_value), _), var_name_search),
               _), var_value_search), _), var_result), _), json_field_name), _) = parsed
        return SumIfExpr(model, manager, signo, var_name, var_value, var_name_search, var_value_search, var_result,
                         json_field_name)

    return keyword('sumif') + keyword('(') + \
           option() + keyword(',') + option() + keyword(',') + option() + keyword(',') + option() + keyword(',') + \
           option() + keyword(',') + option() + keyword(',') + \
           (num_int ^ (lambda i: IntAexp(i)) | (variable ^ (lambda v: VarAexp(v)))) + keyword(',') + option() + \
           keyword(',') + option() + keyword(')') ^ process


def orm_count_if_exp():
    def process(parsed):
        (((((((((((((((((_, _), model), _), manager), _), var_name_search), _), var_value_search), _), var_name), _),
              var_value), _), signo), _), json_field_name), _) = parsed
        return CountIfExpr(model, manager, var_name_search, var_value_search, var_name, var_value, signo,
                           json_field_name)

    return keyword('countif') + keyword('(') + \
           option() + keyword(',') + option() + keyword(',') + option() + \
           keyword(',') + option() + keyword(',') + option() + keyword(',') + option() + keyword(',') + \
           option() + keyword(',') + option() + keyword(')') ^ process


def orm_vlookup_exp():
    def process(parsed):
        (((((((((((((((((((_, _), model), _), manager), _), var_name_search), _), var_value_search), _), signo), _),
                var_name), _), var_value), _), var_result), _), json_field_name), _) = parsed
        return VlookupExpr(model, manager, var_name_search, var_value_search, var_name, var_value, signo, var_result,
                           json_field_name)

    return keyword('vlookup') + keyword('(') + \
           option() + keyword(',') + option() + keyword(',') + option() + keyword(',') + option() + \
           keyword(',') + option() + keyword(',') + option() + keyword(',') + option() + \
           keyword(',') + option() + keyword(',') + option() + keyword(')') ^ process


def orm_directlink_exp():
    def process(parsed):
        (((((((((((((((_, _), model), _), manager), _), var_name_search), _), var_value_search), _), row), _),
            var_result), _), json_field_name), _) = parsed
        return DirectLinkExpr(model, manager, var_name_search, var_value_search, row, var_result, json_field_name)

    return keyword('directlink') + keyword('(') + \
           option() + keyword(',') + option() + keyword(',') + option() + keyword(',') + option() + \
           keyword(',') + option() + keyword(',') + option() + keyword(',') + option() + keyword(')') ^ process
