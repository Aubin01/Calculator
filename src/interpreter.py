from parser import parser

def evaluate(input_text):
    try:
        result = parser.parse(input_text)
        return result if result is not None else "Invalid input"
    except ZeroDivisionError as e:
        return f"Error: {e}"  # Division by zero
    except ValueError as e:
        return str(e)  # Handle undefined variables
    except Exception as e:
        return f"Syntax error: {e}"  # Detailed syntax errors
