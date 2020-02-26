import sys
import re
DATE_FORMATS_VALUES = {
    'DD/MM/YYYY': '%d/%m/%Y',
    'MM/DD/YYYY': '%m/%d/%Y',
    'YYYY/MM/DD': '%Y/%m/%d',
    'YYYY/DD/MM': '%Y/%d/%m',
    'DD/YYYY/MM': '%d/%Y/%m',
    'MM/YYYY/DD': '%m/%Y/%d',
    'DD-MM-YYYY': '%d-%m-%Y',
    'MM-DD-YYYY': '%m-%d-%Y',
    'YYYY-MM-DD': '%Y-%m-%d',
    'YYYY-DD-MM': '%Y-%d-%m',
    'DD-YYYY-MM': '%d-%Y-%m',
    'MM-YYYY-DD': '%m-%Y-%d',
    'YYYY.MM.DD': '%Y.%m.%d',
    'MM.DD.YYYY': '%m.%d.%Y',
    'DD.MM.YYYY': '%d.%m.%Y',

}

class ErrorFormula:

    ERROR_ = {
              'NOT_FOUND': '#N/A',
              'ZERO_DIVISION': '#DIV/0',
              'NOT_RECOGNIZE_NAME': '"#NAME?',
              'NULL_VALUE': '#NULL!',
              'INVALID_ARGUMENT': '#NUM!',
              'INVALID_REFERENCE': '#REF!',
              'INVALID_OPERATION': '#VALUE!'
              }

    ERROR_REVERSE_ = {
                      '#N/A':'NOT_FOUND',
                      '#DIV/0':'ZERO_DIVISION',
                       '#NAME?': 'NOT_RECOGNIZE_NAME',
                       '#NULL!':'NULL_VALUE',
                       '#NUM!':'INVALID_ARGUMENT',
                       '#REF!':'INVALID_REFERENCE',
                       '#VALUE!':'INVALID_OPERATION'
                      }

    EXCEL_ERROR_NUM_VALUE = {
                                42:'NOT_FOUND',
                                36 :'INVALID_ARGUMENT',
                                29 : 'NOT_RECOGNIZE_NAME',
                                23 : 'INVALID_REFERENCE',
                                15 :'INVALID_OPERATION',
                                7:'ZERO_DIVISION',
                                0:'NULL_VALUE'
                             }

    EXCEL_ERROR_METHODS = {
                            42:'=NA()',
                          }

    def __init__(self, state):
        if isinstance(state, str):
            self.actual_error = self.ERROR_.get(state)
        else:
            self.description = self.EXCEL_ERROR_NUM_VALUE.get(state)
            self.actual_error = self.ERROR_.get(self.description)

    @classmethod
    def get_value_by_description(cls, state):
        return cls.ERROR_REVERSE_.get(state)

    @classmethod
    def get_description_by_num(cls,  num):
        return cls.EXCEL_ERROR_NUM_VALUE.get(num)

    @classmethod
    def get_method_by_num(cls, num):
        return cls.EXCEL_ERROR_METHODS.get(num)

    @classmethod
    def get_value_by_num(cls, num):
        return cls.ERROR_.get(cls.get_description_by_num(num))


BOOL_VALUES = {"True": True,
               "False": False}

RESERVED = 'RESERVED'
INT = 'INT'
FLOAT = 'FLOAT'
ID = 'ID'
PUNTO = 'PUNTO'
STRING = 'STRING'
DATE = 'DATE'
BOOL = 'BOOLEAN'

token_exprs = [
    (r"[0-9]{2}\/[0-9]{2}\/[0-9]{4}", DATE),
    (r"[0-9]{4}\/[0-9]{2}\/[0-9]{2}", DATE),
    (r"[0-9]{2}\/[0-9]{4}\/[0-9]{2}", DATE),

    (r"[0-9]{2}\-[0-9]{2}\-[0-9]{4}", DATE),
    (r"[0-9]{4}\-[0-9]{2}\-[0-9]{2}", DATE),
    (r"[0-9]{2}\-[0-9]{4}\-[0-9]{2}", DATE),

    (r"[0-9]{2}\.[0-9]{2}\.[0-9]{4}", DATE),
    (r"[0-9]{4}\.[0-9]{2}\.[0-9]{2}", DATE),
    (r"[0-9]{2}\.[0-9]{4}\.[0-9]{2}", DATE),


    (r'[ \n\t]+', None),
    (r'#[^\n]*', None),
    (r'\:=', RESERVED),
    (r'\(', RESERVED),
    (r'\)', RESERVED),
    (r';', RESERVED),
    (r'\+', RESERVED),
    (r'DATE', RESERVED),
    (r'TRUE', BOOL),
    (r'FALSE', BOOL),
    (r',', RESERVED),
    (r'-', RESERVED),
    (r'\*', RESERVED),
    (r'/', RESERVED),
    (r'<=', RESERVED),
    (r'<', RESERVED),
    (r'>=', RESERVED),
    (r'>', RESERVED),
    (r'!=', RESERVED),
    (r'=', RESERVED),
    (r'AND', RESERVED),
    (r'OR', RESERVED),
    (r'NOT', RESERVED),
    (r'IF', RESERVED),
    (r':', RESERVED),
    (r'SLICE', RESERVED),
    (r'SUMIF', RESERVED),
    (r'CONCAT', RESERVED),
    (r'ERROR', RESERVED),
    (r'DIRECTLINK', RESERVED),
    (r'SPLIT', RESERVED),
    (r'LEN', RESERVED),
    (r'COUNTIF', RESERVED),
    (r'VLOOKUP', RESERVED),
    (r'-?[0-9]+\.[0-9]+', FLOAT),
    (r'-?[0-9]+', INT),
    (r'\.', PUNTO),
    (r"'.*?'", STRING),
    (r'".*?"', STRING),
    (r'[A-Za-z0-9_-][A-Za-z0-9_-]*', ID)
]

