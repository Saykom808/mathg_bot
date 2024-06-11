import sympy as sp


def differentiate_function(expression, variable):
    x = sp.symbols(variable)
    expr = sp.sympify(expression)
    derivative = sp.diff(expr, x)
    return str(derivative)

# def integrate_function(expression, variable):
#     x = sp.symbols(variable)
#     expr = sp.sympify(expression)
#     integral = sp.integrate(expr, x)
#     return str(integral)

# def definite_integral(expression, variable, lower_limit, upper_limit):
#     x = sp.symbols(variable)
#     expr = sp.sympify(expression)
#     integral = sp.integrate(expr, (x, lower_limit, upper_limit))
#     return str(integral)