from manim import *
import sympy as sp  # For parsing and handling equations
import numpy as np  # For numerical evaluation

# This script creates a static 2D coordinate system and plots a function as a static graph using Manim's Axes.
# Step 4: Plot the function as a static graph.
# To render this scene, run:
#   manim -pql manim_plot_2d_equation.py StaticAxesScene

class StaticAxesScene(Scene):
    def construct(self):
        # Create axes with specified x and y ranges
        axes = Axes(
            x_range=[-5, 5, 1],  # x-axis from -5 to 5, tick every 1 unit
            y_range=[-3, 3, 1],  # y-axis from -3 to 3, tick every 1 unit
            axis_config={"color": WHITE}  # Set axis color to white
        )
        # Add the axes to the scene
        self.add(axes)
        # Create and add x-axis and y-axis labels
        x_label = axes.get_x_axis_label(Tex("x"))  # Label for x-axis
        y_label = axes.get_y_axis_label(Tex("y"))  # Label for y-axis
        self.add(x_label, y_label)

        # --- Step 3: Parse and prepare the equation ---
        # Define the equation as a string (can be replaced with user input)
        equation_str = "sin(x) + x**2"  # Example: y = sin(x) + x^2
        x = sp.symbols('x')  # Define the symbol x for sympy
        try:
            # Parse the equation string into a sympy expression
            expr = sp.sympify(equation_str)
            # Convert the sympy expression to a numpy-compatible function
            func = sp.lambdify(x, expr, modules=["numpy", {"sp": np}])
            # Generate a few sample x values
            sample_x = np.linspace(-2, 2, 5)
            # Evaluate the function at the sample x values
            sample_y = func(sample_x)
            # Print the parsed expression and sample values for verification
            print(f"Parsed equation: y = {expr}")
            print("Sample x values:", sample_x)
            print("Sample y values:", sample_y)
        except Exception as e:
            print(f"Error parsing or evaluating the equation: {e}")
            return  # Stop if parsing fails

        # --- Step 4: Plot the function as a static graph ---
        # Define the function to plot (must accept a float and return a float)
        def manim_func(x_val):
            try:
                return func(x_val)
            except Exception:
                return 0  # Return 0 if function fails (avoid errors)

        # Plot the function on the axes
        graph = axes.plot(
            manim_func,
            color=YELLOW,
            x_range=[-5, 5],  # Plot over the same x-range as axes
        )
        # Add the function graph to the scene
        self.add(graph)
        # Optionally, add a label for the function
        # The label must be in LaTeX math mode (wrapped in $...$)
        func_label = axes.get_graph_label(graph, label=Tex(r"$y = \sin(x) + x^2$"), x_val=2)
        self.add(func_label) 