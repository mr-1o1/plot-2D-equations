from manim import *
import sympy as sp  # For parsing and handling equations
import numpy as np  # For numerical evaluation

# This script creates a static 2D coordinate system and animates the drawing of a function graph using Manim's Axes.
# Step 6: Add a moving tip marker that follows the graph as it is drawn.
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

        # --- Step 6: Add a moving tip marker ---
        # Create a Dot at the start of the graph
        start_x = -5
        start_y = manim_func(start_x)
        tip_marker = Dot(axes.c2p(start_x, start_y), color=RED, radius=0.08)
        self.add(tip_marker)

        # Function to update the marker's position as the graph is drawn
        def update_marker(mob, alpha):
            # alpha goes from 0 to 1 during the animation
            # Get the corresponding x value
            x_val = start_x + (5 - (-5)) * alpha  # x from -5 to 5
            y_val = manim_func(x_val)
            mob.move_to(axes.c2p(x_val, y_val))

        # Animate the graph and the marker together
        self.play(
            Create(graph),
            UpdateFromAlphaFunc(tip_marker, update_marker),
            run_time=10
        )
        self.wait(0.5)

        # Optionally, add a label for the function after the animation
        func_label = axes.get_graph_label(graph, label=Tex(r"$y = \sin(x) + x^2$"), x_val=2)
        self.add(func_label) 