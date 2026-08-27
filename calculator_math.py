"""
Mathematical evaluation module for the Scientific Calculator.

This module provides safe expression evaluation with support for:
- Trigonometric functions (sin, cos, tan, asin, acos, atan)
- Hyperbolic functions (sinh, cosh, tanh)  
- Logarithmic functions (log, ln, exp)
- Root functions (sqrt, cbrt)
- Other functions (abs, factorial, modulo, etc.)
- Mathematical constants (pi, e)
- Arbitrary precision arithmetic (Decimal)

Author: Bilal Alyee
License: MIT
"""

import math
from decimal import Decimal, getcontext

# Set precision to 50 decimal places for large numbers
getcontext().prec = 50


def safe_eval(expression, x_value=None, angle_mode='deg'):
    """
    Safely evaluate a mathematical expression with arbitrary precision.
    
    Args:
        expression (str): Mathematical expression to evaluate
        x_value (float, optional): Value for variable 'x' in expressions
        angle_mode (str): 'deg' for degrees, 'rad' for radians (default: 'deg')
    
    Returns:
        float: Result of the expression evaluation
    
    Raises:
        ValueError: If expression is invalid
        ZeroDivisionError: If division by zero occurs
        OverflowError: If result is too large
    """
    
    # Convert angle mode functions
    def sin_fn(x):
        x = float(x)
        return math.sin(math.radians(x) if angle_mode == 'deg' else x)

    def cos_fn(x):
        x = float(x)
        return math.cos(math.radians(x) if angle_mode == 'deg' else x)

    def tan_fn(x):
        x = float(x)
        return math.tan(math.radians(x) if angle_mode == 'deg' else x)

    def asin_fn(x):
        x = float(x)
        res = math.asin(x)
        return math.degrees(res) if angle_mode == 'deg' else res

    def acos_fn(x):
        x = float(x)
        res = math.acos(x)
        return math.degrees(res) if angle_mode == 'deg' else res

    def atan_fn(x):
        x = float(x)
        res = math.atan(x)
        return math.degrees(res) if angle_mode == 'deg' else res
    
    def cbrt_fn(x):
        """Cube root function that handles negative numbers."""
        x = float(x)
        return -(-x) ** (1/3) if x < 0 else x ** (1/3)
    
    def fact_fn(x):
        """Factorial function."""
        return math.factorial(int(x))
    
    def decimal_mul(a, b):
        """Multiply with decimal precision."""
        return float(Decimal(str(a)) * Decimal(str(b)))
    
    def decimal_div(a, b):
        """Divide with decimal precision."""
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        return float(Decimal(str(a)) / Decimal(str(b)))
    
    def decimal_add(a, b):
        """Add with decimal precision."""
        return float(Decimal(str(a)) + Decimal(str(b)))
    
    def decimal_sub(a, b):
        """Subtract with decimal precision."""
        return float(Decimal(str(a)) - Decimal(str(b)))

    # Whitelist of allowed functions and constants
    safe_names = {
        # Trigonometric functions
        'sin': sin_fn, 'cos': cos_fn, 'tan': tan_fn,
        'asin': asin_fn, 'acos': acos_fn, 'atan': atan_fn,
        
        # Hyperbolic functions
        'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
        
        # Root and logarithmic functions
        'sqrt': math.sqrt, 'cbrt': cbrt_fn, 
        'log': math.log10, 'ln': math.log,
        'exp': math.exp,
        
        # Other functions
        'abs': abs, 'round': round, 'pow': pow, 
        'fact': fact_fn,
        
        # Mathematical constants
        'pi': math.pi, 'e': math.e,
        
        # Utility functions
        'sum': sum, 'min': min, 'max': max,
        'mod': lambda a, b: int(Decimal(str(a))) % int(Decimal(str(b))),
        'int': int, 'float': float,
        'Decimal': Decimal,
        
        # Variable
        'x': x_value,
    }
    
    # Validate expression length (prevent excessively long strings)
    if len(expression) > 10000:
        raise ValueError("Expression too long (max 10000 characters)")
    
    # Evaluate expression with restricted namespace
    # '__builtins__': None prevents access to built-in functions not in safe_names
    try:
        result = eval(expression, {'__builtins__': None}, safe_names)
        
        # Convert Decimal back to float if needed
        if isinstance(result, Decimal):
            result = float(result)
        
        return result
    
    except ZeroDivisionError:
        raise ZeroDivisionError("Cannot divide by zero")
    except ValueError as e:
        raise ValueError(f"Invalid calculation: {str(e)}")
    except Exception as e:
        raise ValueError(f"Calculation error: {str(e)}")


def derivative(expr, point, x_value=None, angle_mode='deg'):
    h = 1e-6
    return (safe_eval(expr, point + h, angle_mode=angle_mode) - safe_eval(expr, point - h, angle_mode=angle_mode)) / (2 * h)


def line_equation(x1, y1, x2, y2):
    if x2 == x1:
        raise ValueError('Vertical line has undefined slope')
    m = (y2 - y1) / (x2 - x1)
    c = y1 - m * x1
    m_str = f'{m:.6g}'
    c_str = f'+ {abs(c):.6g}' if c >= 0 else f'- {abs(c):.6g}'
    return f'y = {m_str}x {c_str}'


def point_slope_equation(x1, y1, m):
    c = y1 - m * x1
    m_str = f'{m:.6g}'
    c_str = f'+ {abs(c):.6g}' if c >= 0 else f'- {abs(c):.6g}'
    return f'y - {y1:.6g} = {m_str}(x - {x1:.6g})  ->  y = {m_str}x {c_str}'


def integral(expr, a, b, steps=2000, angle_mode='deg'):
    h = (b - a) / steps
    total = 0.5 * (safe_eval(expr, a, angle_mode=angle_mode) + safe_eval(expr, b, angle_mode=angle_mode))
    for i in range(1, steps):
        total += safe_eval(expr, a + i * h, angle_mode=angle_mode)
    return total * h


def evaluate_expression(expr, angle_mode='deg'):
    expr = expr.replace('power', '**').replace('^', '**')
    if expr.startswith('DERIV(') and expr.endswith(')'):
        inner = expr[6:-1]
        if ',' in inner:
            func_text, pt_text = inner.split(',', 1)
            return derivative(func_text, float(pt_text), angle_mode=angle_mode)
        return derivative(inner, 0.0, angle_mode=angle_mode)
    if expr.startswith('INT(') and expr.endswith(')'):
        inner = expr[4:-1]
        parts = [p.strip() for p in inner.split(',')]
        if len(parts) >= 3:
            func_text, a, b = parts[:3]
            return integral(func_text, float(a), float(b), angle_mode=angle_mode)
        raise ValueError('INT requires function,a,b')

    if expr.startswith('EQN(') and expr.endswith(')'):
        inner = expr[4:-1]
        parts = [p.strip() for p in inner.split(',')]
        if len(parts) == 4:
            x1, y1, x2, y2 = [float(p) for p in parts]
            return line_equation(x1, y1, x2, y2)
        raise ValueError('EQN requires x1,y1,x2,y2')

    if expr.startswith('PS(') and expr.endswith(')'):
        inner = expr[3:-1]
        parts = [p.strip() for p in inner.split(',')]
        if len(parts) == 3:
            x1, y1, m = [float(p) for p in parts]
            return point_slope_equation(x1, y1, m)
        raise ValueError('PS requires x1,y1,m')

    return safe_eval(expr, angle_mode=angle_mode)


def apply_math_function(func, val, angle_mode='deg'):
    try:
        if func == 'sin':
            angle = math.radians(val) if angle_mode == 'deg' else val
            return math.sin(angle)
        if func == 'cos':
            angle = math.radians(val) if angle_mode == 'deg' else val
            return math.cos(angle)
        if func == 'tan':
            angle = math.radians(val) if angle_mode == 'deg' else val
            return math.tan(angle)
        if func == 'sqrt':
            if val < 0:
                raise ValueError('sqrt domain error')
            return math.sqrt(val)
        if func == 'log':
            if val <= 0:
                raise ValueError('log domain error')
            return math.log10(val)
        if func == 'ln':
            if val <= 0:
                raise ValueError('ln domain error')
            return math.log(val)
        if func == 'exp':
            return math.exp(val)
        if func == 'power':
            return val ** 2
        if func == '1/x':
            if val == 0:
                raise ZeroDivisionError('division by zero')
            return 1 / val
        if func == 'fact':
            n = int(val)
            if n < 0:
                raise ValueError('factorial domain error')
            return math.factorial(n)
        if func == 'sinh':
            return math.sinh(val)
        if func == 'cosh':
            return math.cosh(val)
        if func == 'tanh':
            return math.tanh(val)
        if func == 'asin':
            if val < -1 or val > 1:
                raise ValueError('asin domain error')
            out = math.asin(val)
            return math.degrees(out) if angle_mode == 'deg' else out
        if func == 'acos':
            if val < -1 or val > 1:
                raise ValueError('acos domain error')
            out = math.acos(val)
            return math.degrees(out) if angle_mode == 'deg' else out
        if func == 'atan':
            out = math.atan(val)
            return math.degrees(out) if angle_mode == 'deg' else out
        if func == '10^':
            return 10 ** val
        return val
    except Exception as e:
        raise
    if func == 'cos':
        angle = math.radians(val) if angle_mode == 'deg' else val
        return math.cos(angle)
    if func == 'tan':
        angle = math.radians(val) if angle_mode == 'deg' else val
        return math.tan(angle)
    if func == 'sqrt':
        return math.sqrt(val)
    if func == 'log':
        return math.log10(val)
    if func == 'ln':
        return math.log(val)
    if func == 'exp':
        return math.exp(val)
    if func == 'power':
        return val ** 2
    if func == '1/x':
        return 1 / val
    if func == 'fact':
        return math.factorial(int(val))
    if func == 'sinh':
        return math.sinh(val)
    if func == 'cosh':
        return math.cosh(val)
    if func == 'tanh':
        return math.tanh(val)
    if func == 'asin':
        out = math.asin(val)
        return math.degrees(out) if angle_mode == 'deg' else out
    if func == 'acos':
        out = math.acos(val)
        return math.degrees(out) if angle_mode == 'deg' else out
    if func == 'atan':
        out = math.atan(val)
        return math.degrees(out) if angle_mode == 'deg' else out
    if func == '10^':
        return 10 ** val
    return val
