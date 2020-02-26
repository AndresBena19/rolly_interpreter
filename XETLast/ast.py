from __future__ import division
from datetime import datetime
from XETLlexer.tokens import DATE_FORMATS_VALUES
from uuid import uuid4


class Equality:

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)


class Statement(Equality):
    pass


class Aexp(Equality):
    pass


class Bexp(Equality):
    pass


class Sexp(Equality):
    pass


class AssignStatement(Statement):
    def __init__(self, name, aexp):
        self.name = name
        self.aexp = aexp
        self.key = uuid4()

    def __repr__(self):
        return 'AssignStatement(%s, %s)' % (self.name, self.aexp)

    def eval(self, env):
        value = self.aexp.eval(env)
        env[self.name] = value


class CompoundStatement(Statement):
    def __init__(self, first, second):
        self.first = first
        self.second = second
        self.key = uuid4()

    def __repr__(self):
        return 'CompoundStatement(%s, %s)' % (self.first, self.second)

    def eval(self, env):
        self.first.eval(env)
        self.second.eval(env)


class IfStatement(Statement):
    def __init__(self, condition, true_stmt, false_stmt):
        self.condition = condition
        self.true_stmt = true_stmt
        self.false_stmt = false_stmt
        self.key = uuid4()

    def __repr__(self):
        return 'IfStatement({}, {}, {})'.format(self.condition, self.true_stmt, self.false_stmt)

    def eval(self, env):
        condition_value = self.condition.eval(env)
        if condition_value:
            self.true_stmt.eval(env)
        else:
            if self.false_stmt:
                self.false_stmt.eval(env)


class IntAexp(Aexp):
    def __init__(self, value):
        self.value = value
        self.key = uuid4()

    def __repr__(self):
        return 'IntAexp({})'.format(self.value)

    def eval(self, env):
        return self.value


class DateAexp(Aexp):
    def __init__(self, value, format=None):
        self.value = value
        self.format = format
        self.key = uuid4()

    def __repr__(self):
        return 'DateAexp({})'.format(self.value)

    def eval(self, env):
        if self.format in env:
            self.format = env[self.format]
        if self.value in env:
            self.value = env[self.i]

        return datetime.strptime(self.value, DATE_FORMATS_VALUES.get(self.format))


class FloatAexp():
    def __init__(self, value):
        self.value = value
        self.key = uuid4()

    def __repr__(self):
        return 'FloatAexp({})'.format(self.value)

    def eval(self, env):
        return self.value


class BoolAexp():
    def __init__(self, value):
        self.value = value
        self.key = uuid4()

    def __repr__(self):
        return 'BoolAexp({})'.format(self.value)

    def eval(self, env):
        return self.value


class StringAexp():
    def __init__(self, value):
        self.value = value
        self.key = uuid4()

    def __repr__(self):
        return 'StringAexp({})'.format(self.value)

    def eval(self, env):
        return self.value


class VarAexp(Aexp):
    def __init__(self, value):
        self.value = value
        self.key = uuid4()

    def __repr__(self):
        return 'VarAexp({})'.format(self.value)

    def eval(self, env):
        if self.value in env:
            return env[self.value]
        else:
            return 0


class BinopAexp(Aexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
        self.key = uuid4()

    def __repr__(self):
        return 'BinopAexp({}, {}, {})'.format(self.op, self.left, self.right)

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)

        if self.op == '+':
            value = left_value + right_value
        elif self.op == '-':
            value = left_value - right_value
        elif self.op == '*':
            value = left_value * right_value
        elif self.op == '/':
            value = left_value / right_value
        else:
            raise RuntimeError('unknown operator: ' + self.op)
        return value


class RelopBexp(Bexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return 'RelopBexp({}, {}, {})'.format(self.op, self.left, self.right)

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        if self.op == '<':
            value = left_value < right_value
        elif self.op == '<=':
            value = left_value <= right_value
        elif self.op == '>':
            value = left_value > right_value
        elif self.op == '>=':
            value = left_value >= right_value
        elif self.op == '=':
            value = left_value == right_value
        elif self.op == '!=':
            value = left_value != right_value
        else:
            raise RuntimeError('unknown operator: ' + self.op)
        return value


class AndBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.key = uuid4()

    def __repr__(self):
        return 'AndBexp({}, {})'.format(self.left, self.right)

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        return left_value and right_value


class OrBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.key = uuid4()

    def __repr__(self):
        return 'OrBexp({}, {})'.format(self.left, self.right)

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        return left_value or right_value


class NotBexp(Bexp):
    def __init__(self, exp):
        self.exp = exp
        self.key = uuid4()

    def __repr__(self):
        return 'NotBexp({})'.format(self.exp)

    def eval(self, env, memorized=None):
        value = self.exp.eval(env, memorized)
        if isinstance(value, ErrorExpr):
            return value
        else:
            return not value


class SliceExpr(Sexp):

    def __init__(self, value, start, end):
        self.value = value
        self.start = start
        self.end = end
        self.key = uuid4()

    def __repr__(self):
        return 'SlicedSexp({})'.format(self.value)

    def eval(self, env, memorized=None):
        pass


class ConcatExpr(Sexp):

    def __init__(self, string_1, string_2, string_3):
        self.string_1 = string_1
        self.string_2 = string_2
        self.string_3 = string_3
        self.key = uuid4()

    def __repr__(self):
        return 'ConcatSexp({})'.format(self.string_1)

    def eval(self, env, memorized=None):
        pass

    def transform_number(self, value):
        try:
            value_decimal = float(value)
            if value_decimal.is_integer():
                return int(value_decimal)
            else:
                return str(value_decimal)

        except Exception as e:
            return value


class SplitExtractExpr(Sexp):

    def __init__(self, data_text, simbol, segment):
        self.data_text = data_text
        self.simbol = simbol
        self.segment = segment
        self.key = uuid4()

    def __repr__(self):
        return 'SplitExtractExpr({})'.format(self.data_text)

    def eval(self, env, memorized=None):
        pass


class LenExpr(Sexp):

    def __init__(self, value):
        self.value = value
        self.key = uuid4()

    def __repr__(self):
        return 'LenSexp({})'.format(self.value)

    def eval(self, env, memorized=None):
        pass


class ErrorExpr(Sexp):

    def __init__(self, value):
        self.value = value
        self.type = "ERROR"
        self.key = uuid4()

    def __repr__(self):
        return 'ErrorSexp({})'.format(self.value)

    def eval(self, env, memorized=None):
        pass
