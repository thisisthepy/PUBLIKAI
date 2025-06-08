def calculate(expression: str) -> str:
    """
    Evaluate a mathematical expression and return the result as a string.

    Args:
        expression (str): The mathematical expression to evaluate.

    Returns:
        str: The result of the evaluation or an error message if the expression is invalid.
    """
    try:
        # Evaluate the expression safely
        result = eval(expression, {"__builtins__": None}, {})
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"
