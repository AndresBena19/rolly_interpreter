import unittest

from XETLlexer.lexer import lexer


class TestLexer(unittest.TestCase):
    def setUp(self):
        self.lexer = lambda text: lexer(text)

    def tearDown(self):
        del self.lexer

    def test_variable(self):
        variable = """variable := other_variable"""
        tokens = self.lexer(variable)
        first_variable, sign_reserved, second_variable = tokens

        self.assertEqual(first_variable, ('variable', 'ID'))
        self.assertEqual(sign_reserved, (':=', 'RESERVED'))
        self.assertEqual(second_variable, ('other_variable', 'ID'))

    def test_integer(self):
        integer = """integer:=2"""
        tokens = self.lexer(integer)
        first_variable, sign_reserved, integer_value = tokens

        self.assertEqual(first_variable, ('integer', 'ID'))
        self.assertEqual(sign_reserved, (':=', 'RESERVED'))
        self.assertEqual(integer_value, ('2', 'INT'))

    def test_integer_more_digits(self):
        integer = """integer:=28237872361283687123878712368721783218368716378126783681276387123"""
        tokens = self.lexer(integer)
        first_variable, sign_reserved, integer_value = tokens

        self.assertEqual(first_variable, ('integer', 'ID'))
        self.assertEqual(sign_reserved, (':=', 'RESERVED'))
        self.assertEqual(integer_value, ('28237872361283687123878712368721783218368716378126783681276387123', 'INT'))

    def test_float(self):
        float_text = """float:=2.0"""
        tokens = self.lexer(float_text)
        first_variable, sign_reserved, float_value = tokens

        self.assertEqual(first_variable, ('float', 'ID'))
        self.assertEqual(sign_reserved, (':=', 'RESERVED'))
        self.assertEqual(float_value, ('2.0', 'FLOAT'))

    def test_float_with_more_decimal_values(self):
        float_text = """float:=2.9283982173882380"""
        tokens = self.lexer(float_text)
        first_variable, sign_reserved, float_value = tokens

        self.assertEqual(first_variable, ('float', 'ID'))
        self.assertEqual(sign_reserved, (':=', 'RESERVED'))
        self.assertEqual(float_value, ('2.9283982173882380', 'FLOAT'))

    def test_string_with_single_quotes(self):
        text = """string:='lorem ipsum'"""""
        tokens = self.lexer(text)
        first_variable, sign_reserved, string_value = tokens

        self.assertEqual(first_variable, ('string', 'ID'))
        self.assertEqual(sign_reserved, (':=', 'RESERVED'))
        self.assertEqual(string_value, ("'lorem ipsum'", 'STRING'))

    def test_string_with_double_quotes(self):
        text = 'string:="lorem ipsum"'
        tokens = self.lexer(text)
        first_variable, sign_reserved, string_value = tokens

        self.assertEqual(first_variable, ('string', 'ID'))
        self.assertEqual(sign_reserved, (':=', 'RESERVED'))
        self.assertEqual(string_value, ('"lorem ipsum"', 'STRING'))

    def test_boolean_true_statement(self):
        boolean = 'bool:=TRUE'
        tokens = self.lexer(boolean)
        first_variable, sign_reserved, boolean_value = tokens

        self.assertEqual(first_variable, ('bool', 'ID'))
        self.assertEqual(sign_reserved, (':=', 'RESERVED'))
        self.assertEqual(boolean_value, ('TRUE', 'BOOLEAN'))

    def test_boolean_false_statement(self):
        boolean = 'bool:=FALSE'
        tokens = self.lexer(boolean)
        first_variable, sign_reserved, boolean_value = tokens

        self.assertEqual(first_variable, ('bool', 'ID'))
        self.assertEqual(sign_reserved, (':=', 'RESERVED'))
        self.assertEqual(boolean_value, ('FALSE', 'BOOLEAN'))

    def test_date(self):
        date = """date := DATE(2020/02/01, "YYYY/MM/DD")"""
        tokens = self.lexer(date)
        first_variable, sign_reserved, reserved_date, sign_open, \
        date_value, comma, format_value, sign_close = tokens

        self.assertEqual(first_variable, ('date', 'ID'))
        self.assertEqual(sign_reserved, (':=', 'RESERVED'))
        self.assertEqual(reserved_date, ('DATE', 'RESERVED'))
        self.assertEqual(sign_open, ('(', 'RESERVED'))
        self.assertEqual(date_value, ('2020/02/01', 'DATE'))
        self.assertEqual(comma, (',', 'RESERVED'))
        self.assertEqual(format_value, ('"YYYY/MM/DD"', 'STRING'))
        self.assertEqual(sign_close, (')', 'RESERVED'))

    def test_negative_integer(self):
        integer = """integer:=-2"""
        tokens = self.lexer(integer)
        first_variable, sign_reserved, integer_value = tokens

        self.assertEqual(first_variable, ('integer', 'ID'))
        self.assertEqual(sign_reserved, (':=', 'RESERVED'))
        self.assertEqual(integer_value, ('-2', 'INT'))

    def test_negative_integer_more_digits(self):
        integer = """integer:=-28237872361283687123878712368721783218368716378126783681276387123"""
        tokens = self.lexer(integer)
        first_variable, sign_reserved, integer_value = tokens

        self.assertEqual(first_variable, ('integer', 'ID'))
        self.assertEqual(sign_reserved, (':=', 'RESERVED'))
        self.assertEqual(integer_value, ('-28237872361283687123878712368721783218368716378126783681276387123', 'INT'))

    def test_negative_float(self):
        float_text = """float:=-2.0"""
        tokens = self.lexer(float_text)
        first_variable, sign_reserved, float_value = tokens

        self.assertEqual(first_variable, ('float', 'ID'))
        self.assertEqual(sign_reserved, (':=', 'RESERVED'))
        self.assertEqual(float_value, ('-2.0', 'FLOAT'))

    def test_negative_float_with_more_decimal_values(self):
        float_text = """float:=-2.9283982173882380"""
        tokens = self.lexer(float_text)
        first_variable, sign_reserved, float_value = tokens

        self.assertEqual(first_variable, ('float', 'ID'))
        self.assertEqual(sign_reserved, (':=', 'RESERVED'))
        self.assertEqual(float_value, ('-2.9283982173882380', 'FLOAT'))

    def test_negative_integer_in_complex_expression(self):
        integer = """integer:=-2 + (1 * 3 / (1 * 3) - 4)"""
        tokens = self.lexer(integer)
        variable1, sign_reserved, negative_integer1, \
        operator_plus1, sign_open1, integer1, \
        operator_mul1, integer2, operator_div1, sign_open2, \
        integer3, operator_mul2, integer4, \
        sign_close1, operator_minu1, integer5, sign_close2 = tokens

        self.assertEqual(variable1, ('integer', 'ID'))
        self.assertEqual(sign_reserved, (':=', 'RESERVED'))
        self.assertEqual(negative_integer1, ('-2', 'INT'))
        self.assertEqual(operator_plus1, ('+', 'RESERVED'))
        self.assertEqual(sign_open1, ('(', 'RESERVED'))
        self.assertEqual(integer1, ('1', 'INT'))
        self.assertEqual(operator_mul1, ('*', 'RESERVED'))
        self.assertEqual(integer2, ('3', 'INT'))
        self.assertEqual(operator_div1, ('/', 'RESERVED'))
        self.assertEqual(sign_open2, ('(', 'RESERVED'))
        self.assertEqual(integer3, ('1', 'INT'))
        self.assertEqual(operator_mul2, ('*', 'RESERVED'))
        self.assertEqual(integer4, ('3', 'INT'))
        self.assertEqual(sign_close1, (')', 'RESERVED'))
        self.assertEqual(operator_minu1, ('-', 'RESERVED'))
        self.assertEqual(integer5, ('4', 'INT'))
        self.assertEqual(sign_close2, (')', 'RESERVED'))

    def test_negative_float_in_complex_expression(self):
        float_value = """integer:=-2.8212 + (1 * 3 / (1 * 3) - 1.233)"""

        tokens = self.lexer(float_value)
        variable1, sign_reserved, negative_float1, \
        operator_plus1, sign_open1, integer1, \
        operator_mul1, integer2, operator_div1, \
        sign_open2, integer3, operator_mul2, integer4, \
        sign_close1, operator_minu1, float2, sign_close2 = tokens

        self.assertEqual(variable1, ('integer', 'ID'))
        self.assertEqual(sign_reserved, (':=', 'RESERVED'))
        self.assertEqual(negative_float1, ('-2.8212', 'FLOAT'))
        self.assertEqual(operator_plus1, ('+', 'RESERVED'))
        self.assertEqual(sign_open1, ('(', 'RESERVED'))
        self.assertEqual(integer1, ('1', 'INT'))
        self.assertEqual(operator_mul1, ('*', 'RESERVED'))
        self.assertEqual(integer2, ('3', 'INT'))
        self.assertEqual(operator_div1, ('/', 'RESERVED'))
        self.assertEqual(sign_open2, ('(', 'RESERVED'))
        self.assertEqual(integer3, ('1', 'INT'))
        self.assertEqual(operator_mul2, ('*', 'RESERVED'))
        self.assertEqual(integer4, ('3', 'INT'))
        self.assertEqual(sign_close1, (')', 'RESERVED'))
        self.assertEqual(operator_minu1, ('-', 'RESERVED'))
        self.assertEqual(float2, ('1.233', 'FLOAT'))
        self.assertEqual(sign_close2, (')', 'RESERVED'))

    def test_if_expression(self):
        if_statement = """condition := IF(1.2 > 1;  "OK"; "NOT")"""

        tokens = self.lexer(if_statement)

        condition, reserved, reserved_if, sign_open,\
        float_value, operation_grather, int_value, \
        reserved_separato1, string1, reserved_separator2, \
        string2, sign_close = tokens

        self.assertEqual(condition, ('condition', 'ID'))
        self.assertEqual(reserved,  (':=', 'RESERVED'))
        self.assertEqual(reserved_if, ('IF', 'RESERVED'))
        self.assertEqual(sign_open, ('(', 'RESERVED'))
        self.assertEqual(float_value,  ('1.2', 'FLOAT'))
        self.assertEqual(operation_grather, ('>', 'RESERVED'))
        self.assertEqual(int_value, ('1', 'INT'),)
        self.assertEqual(reserved_separato1, (';', 'RESERVED'))
        self.assertEqual(string1, ('"OK"', 'STRING'),)
        self.assertEqual(reserved_separator2,  (';', 'RESERVED'))
        self.assertEqual(string2, ('"NOT"', 'STRING'))
        self.assertEqual(sign_close, (')', 'RESERVED'))
