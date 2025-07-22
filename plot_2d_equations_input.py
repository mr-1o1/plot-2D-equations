import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

# Prompt user for equation
print("Enter a 2D equation in terms of x (e.g., sin(x) + x**2):")
equation_str = input("y = ")

# Prompt user for x-range
print("Enter the x-range for plotting:")
x_min = float(input("x min: "))
x_max = float(input("x max: "))

# Parse the equation
x = sp.symbols('x')
try:
    expr = sp.sympify(equation_str)
    func = sp.lambdify(x, expr, modules=["numpy"])
    print("Equation parsed successfully.")
except Exception as e:
    print(f"Error parsing equation: {e}")
    func = None

# For demonstration, print the parsed expression and range
print(f"Parsed equation: y = {expr}")
print(f"x-range: {x_min} to {x_max}")

# Step 2: Generate data points
if func is not None:
    x_vals = np.linspace(x_min, x_max, 500)
    try:
        y_vals = func(x_vals)
        # If y_vals is a scalar, broadcast to array
        if np.isscalar(y_vals):
            y_vals = np.full_like(x_vals, y_vals, dtype=float)
        print("First 5 x values:", x_vals[:5])
        print("First 5 y values:", y_vals[:5])
    except Exception as e:
        print(f"Error evaluating function: {e}") 