import math


def safe_eval(expression, x_value=None, angle_mode='deg'):
    def sin_fn(x):
        return math.sin(math.radians(x) if angle_mode == 'deg' else x)

    def cos_fn(x):
        return math.cos(math.radians(x) if angle_mode == 'deg' else x)

    def tan_fn(x):
        return math.tan(math.radians(x) if angle_mode == 'deg' else x)

    def asin_fn(x):
        res = math.asin(x)
        return math.degrees(res) if angle_mode == 'deg' else res

    def acos_fn(x):
        res = math.acos(x)
        return math.degrees(res) if angle_mode == 'deg' else res

    def atan_fn(x):
        res = math.atan(x)
        return math.degrees(res) if angle_mode == 'deg' else res
    
    def cbrt_fn(x):
        return -(-x) ** (1/3) if x < 0 else x ** (1/3)
    
    def fact_fn(x):
        return math.factorial(int(x))

    safe_names = {
        'sin': sin_fn, 'cos': cos_fn, 'tan': tan_fn,
        'asin': asin_fn, 'acos': acos_fn, 'atan': atan_fn,
        'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
        'sqrt': math.sqrt, 'cbrt': cbrt_fn, 'log': math.log10, 'ln': math.log,
        'exp': math.exp, 'abs': abs, 'round': round, 'pow': pow, 'fact': fact_fn,
        'pi': math.pi, 'e': math.e,
        'sum': sum, 'min': min, 'max': max,
        'mod': lambda a, b: a % b,
        'int': int, 'float': float,
        'x': x_value,
    }
    return eval(expression, {'__builtins__': None}, safe_names)


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
