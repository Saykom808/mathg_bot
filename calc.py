import sympy as sp

def integrate_function(expression, variable):
    """
    Вычисляет неопределенный интеграл от заданного выражения по заданной переменной.
    
    :param expression: Символьное выражение для интегрирования (например, 'x**2')
    :param variable: Переменная интегрирования (например, 'x')
    :return: Интеграл выражения
    """
    # Преобразуем строковое выражение в символьное
    expr = sp.sympify(expression)
    
    # Определяем переменную интегрирования
    var = sp.symbols(variable)
    
    # Вычисляем неопределенный интеграл
    integral = sp.integrate(expr, var)
    
    return integral

def definite_integral(expression, variable, lower_limit, upper_limit):
    """
    Вычисляет определенный интеграл от заданного выражения по заданной переменной
    в пределах от lower_limit до upper_limit.
    
    :param expression: Символьное выражение для интегрирования (например, 'x**2')
    :param variable: Переменная интегрирования (например, 'x')
    :param lower_limit: Нижний предел интегрирования
    :param upper_limit: Верхний предел интегрирования
    :return: Значение определенного интеграла
    """
    # Преобразуем строковое выражение в символьное
    expr = sp.sympify(expression)
    
    # Определяем переменную интегрирования
    var = sp.symbols(variable)
    
    # Вычисляем определенный интеграл
    integral = sp.integrate(expr, (var, lower_limit, upper_limit))
    
    return integral

if __name__ == "__main__":
    # Пример использования
    expr = "x**2"
    var = "x"
    
    # Неопределенный интеграл
    indefinite_result = integrate_function(expr, var)
    print(f"Неопределенный интеграл {expr} по {var}: {indefinite_result}")
    
    # Определенный интеграл
    lower_limit = 0
    upper_limit = 1
    definite_result = definite_integral(expr, var, lower_limit, upper_limit)
    print(f"Определенный интеграл {expr} по {var} от {lower_limit} до {upper_limit}: {definite_result}")
