import ply.lex as lex

# Tokens
tokens = (
    'NUMBER', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE',
    'LPAREN', 'RPAREN', 'ASSIGN', 'VARIABLE', 'PRINT'
)

# Token patterns
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ASSIGN = r'='
t_VARIABLE = r'[a-zA-Z_][a-zA-Z0-9_]*'

# Reserved words
reserved = {'print': 'PRINT'}

def t_PRINT(t):
    r'print'
    t.type = reserved.get(t.value, 'VARIABLE')  # Check if it's the keyword 'print'
    return t

# Numbers
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# Ignore spaces and tabs
t_ignore = ' \t'

# Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build lexer
lexer = lex.lex()
