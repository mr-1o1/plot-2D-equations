from manim import *

# This script creates a static 2D coordinate system using Manim's Axes.
# Step 2 of the animated 2D equation plotter project.
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