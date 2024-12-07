import ply.yacc as yacc
from lexer import tokens

# Symbol table for storing variables
variables = {}

# Grammar rules
def p_statement_assign(p):
    "statement : VARIABLE ASSIGN expression"
    variables[p[1]] = p[3]
    p[0] = f"{p[1]} = {p[3]}"

def p_statement_expression(p):
    """statement : expression
                 | VARIABLE"""
    if isinstance(p[1], str):  # Check if it's a variable name
        if p[1] in variables:
            p[0] = variables[p[1]]  # Return the variable's value
        else:
            raise ValueError(f"Error: Variable '{p[1]}' is not defined")
    else:
        p[0] = p[1]  # Return the result of an expression

def p_statement_print(p):
    "statement : PRINT LPAREN VARIABLE RPAREN"
    if p[3] in variables:
        p[0] = variables[p[3]]  # Return the variable's value
    else:
        raise ValueError(f"Error: Variable '{p[3]}' is not defined")

def p_expression_binop(p):
    """expression : expression PLUS term
                  | expression MINUS term"""
    p[0] = p[1] + p[3] if p[2] == '+' else p[1] - p[3]

def p_expression_term(p):
    "expression : term"
    p[0] = p[1]

def p_term_binop(p):
    """term : term MULTIPLY factor
            | term DIVIDE factor"""
    if p[2] == '/' and p[3] == 0:
        raise ZeroDivisionError("Error: Division by zero")
    p[0] = p[1] * p[3] if p[2] == '*' else p[1] / p[3]

def p_term_factor(p):
    "term : factor"
    p[0] = p[1]

def p_factor_number(p):
    "factor : NUMBER"
    p[0] = p[1]

def p_factor_variable(p):
    "factor : VARIABLE"
    if p[1] in variables:
        p[0] = variables[p[1]]
    else:
        raise ValueError(f"Error: Variable '{p[1]}' is not defined")

def p_factor_parens(p):
    "factor : LPAREN expression RPAREN"
    p[0] = p[2]

def p_error(p):
    if p:
        print(f"Syntax error at token '{p.value}'")
    else:
        print("Syntax error at EOF")

# Build parser
parser = yacc.yacc()
