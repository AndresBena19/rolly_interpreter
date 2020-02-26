from XETLlexer.tokens import token_exprs
import re


def lexer(characters):
    return lex(characters, token_exprs)


def lex(characters, token_exprs):
    characters = characters.strip()
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
                    # if text in ['and', 'or', 'if', 'date', 'True', 'False', 'not', 'slice', 'sumif', 'concat', 'len', 'countif', 'vlookup', 'directlink', 'split_get', 'error_formula']:
                    #     if len(characters) > match.end(0):
                    #         metadata = lex(characters[match.end(0)],token_exprs)
                    #         if metadata:
                    #             text_reserved, tag_reserved = metadata[0]
                    #             if tag_reserved in ['ID', 'INT', 'STRING']:
                    #                 continue
                    if text == '-':
                        if not tokens:
                            continue
                        text_valid, tag_valid = tokens[-1]
                        if tag_valid in ["INT", "FLOAT", 'ID', 'RESERVED'] and text_valid not in [':=', ';']:
                            pass
                        else:
                            continue
                    token = (text, tag)
                    tokens.append(token)
                break
        if not match:
            print('Illegal character:{}'.format(characters[pos]))

        else:
            pos = match.end(0)
    return tokens