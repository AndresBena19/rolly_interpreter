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
    'MM-YYYY-DD': '%m-%Y-%d'

}

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

    (r'[ \n\t]+', None),
    (r'#[^\n]*', None),
    (r'\:=', RESERVED),
    (r'\(', RESERVED),
    (r'\)', RESERVED),
    (r';', RESERVED),
    (r'\+', RESERVED),
    (r'date', RESERVED),
    (r'True', BOOL),
    (r'False', BOOL),
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
    (r'and', RESERVED),
    (r'or', RESERVED),
    (r'not', RESERVED),
    (r'if', RESERVED),
    (r':', RESERVED),
    (r'[0-9]+\.[0-9]+', FLOAT),
    (r'[0-9]+', INT),
    (r'\.', PUNTO),
    (r'[A-Za-z][A-Za-z0-9_]*', ID),
    (r"'.*?'", STRING),
    (r'".*?"', STRING),
]


def rolly_lex(characters):
    return lex(characters, token_exprs)


def lex(characters, token_exprs):
    pos = 0
    tokens = []
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag:
                    token = (text, tag)
                    tokens.append(token)
                break
        if not match:
            sys.stderr.write('Illegal character: %s\n' % characters[pos])
            sys.exit(1)
        else:
            pos = match.end(0)
    return tokens
