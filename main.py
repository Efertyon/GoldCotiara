import ply.lex as lex
import ply.yacc as yacc

# Лексический анализатор
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'VAR',
    'ID',
    'EQUALS',
    'SEMI',
    'LPAREN',
    'RPAREN',
    'EXIT',
    'ECHO',
    'STRING'
)

# Определение токенов
t_PLUS = r'\+'
t_MINUS = r'-'
t_VAR = r'var'
t_EQUALS = r'='
t_SEMI = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NUMBER = r'\d+'
t_EXIT = r'exit'
t_ECHO = r'echo'
t_STRING = r'"[^"]*"|\'[^\']\''  # added STRING token

# Игнорируем пробелы
t_ignore = ' \t'

# Определение ID
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in reserved:
        t.type = t.value.upper()
    return t

# Обработка ошибок
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Создание лексера
lexer = lex.lex()

# Грамматика и парсер
reserved = {'var', 'exit', 'echo'}

def p_statement_assign(p):
    'statement : VAR ID EQUALS expression SEMI'
    if p[2] in reserved:
        print(f"Error: '{p[2]}' is a reserved word and cannot be used as a variable name")
    else:
        variables[p[2]] = p[4]

def p_statement_expr(p):
    'statement : expression SEMI'
    p[0] = p[1]

def p_statement_exit(p):
    'statement : EXIT SEMI'
    raise SystemExit("Exiting the program")

def p_statement_echo(p):
    'statement : ECHO string SEMI'
    print(p[2][1:-1])  # remove quotes

def p_expression_binop(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = int(p[1])

def p_expression_id(p):
    'expression : ID'
    if p[1] in reserved:
        print(f"Error: '{p[1]}' is a reserved word and cannot be used as a variable name")
        p[0] = 0
    else:
        p[0] = variables.get(p[1], 0)

def p_term(p):
    'term : NUMBER'
    p[0] = int(p[1])

def p_string(p):
    'string : STRING'
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

# Создание парсера
parser = yacc.yacc()

# Переменные
variables = {}

# Пример использования
def parse_expression(expression):
    lexer.input(expression)
    result = parser.parse(expression)
    return result

if __name__ == "__main__":
    while True:
        try:
            s = input('simple_lang > ')
            if s.strip() == 'exit;':
                print("Exiting the program")
                break
            result = parse_expression(s)
            if result is not None:
                print(result)
        except SystemExit as e:
            print(e)
            break