from XETLast.ast import Equality
import uuid

class Sumexp(Equality):
    pass


class SumIfExpr(Sumexp):

    def __init__(self, model, manager, signo, var_name_apply, var_value_apply, var_name_search, var_value_search,
                 var_result, json_field=None):
        self.model = model
        self.manager = manager
        self.signo = signo
        self.var_name_apply = var_name_apply
        self.var_value_apply = var_value_apply
        self.var_value_search = var_value_search
        self.var_result = var_result
        self.var_name_search = var_name_search
        self.key = uuid.uuid1()

        self.json_field = json_field

    def __repr__(self):
        return 'SumIfSexp(%s)' % self.var_result

    def eval(self, env, memorized=None):
        pass


class CountIfExpr(Sumexp):

    def __init__(self, model, manager, var_name_search, var_value_search, var_name, var_value, signo,
                 json_field_name=None):
        self.model = model
        self.manager = manager
        self.signo = signo
        self.var_name_search = var_name_search
        self.var_value_search = var_value_search
        self.var_name = var_name
        self.var_value = var_value
        self.key = uuid.uuid1()

        self.json_field = json_field_name

    def __repr__(self):
        return 'CountIfSexp'


    def eval(self, env, memorized=None):
        pass


class VlookupExpr(Sumexp):

    def __init__(self, model, manager, var_name_search, var_value_search, var_name, var_value, signo, var_result,
                 json_field_name=None):
        self.model = model
        self.manager = manager
        self.signo = signo
        self.var_name_search = var_name_search
        self.var_value_search = var_value_search
        self.var_name = var_name
        self.var_value = var_value
        self.var_result = var_result
        self.key = uuid.uuid1()

        self.json_field = json_field_name

    def __repr__(self):
        return 'VlookUpSexp(%s)' % self.var_result

    def eval(self, env, memorized=None):
        pass


class DirectLinkExpr(Sumexp):

    def __init__(self, model, manager, var_name_search, var_value_search, index, var_result, json_field_name=None):
        self.model = model
        self.manager = manager
        self.var_name_search = var_name_search
        self.var_value_search = var_value_search
        self.var_result = var_result
        self.index = index
        self.json_field = json_field_name
        self.key = uuid.uuid1()

    def __repr__(self):
        return 'DirectLinkSexp(%s)' % self.var_result

    def eval(self, env, memorized=None):
        pass
