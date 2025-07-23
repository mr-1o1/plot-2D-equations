# Import required libraries
import numpy as np  # For numerical operations
import sympy as sp  # For symbolic math and parsing equations
import matplotlib.pyplot as plt  # For plotting
from matplotlib.animation import FuncAnimation  # For animation
import sys

# Prompt user for animation speed
try:
    speed = int(input("Enter animation speed (milliseconds per frame, default 20): ") or 20)
    if speed <= 0:
        print("Speed must be positive. Using default 20.")
        speed = 20
except Exception:
    print("Invalid input. Using default speed 20.")
    speed = 20

# Prompt user for equation
print("Enter the equation for y in terms of x (e.g., sin(x) + x**2):")
equation_str = input("y = ")

# Prompt user for x-range
print("Enter the x-range for plotting:")
x_min = float(input("x min: "))
x_max = float(input("x max: "))

# Parse the equation string into a symbolic expression
x = sp.symbols('x')
try:
    expr = sp.sympify(equation_str)  # Convert string to sympy expression
    func = sp.lambdify(x, expr, modules=["numpy"])  # Make a function for numpy arrays
    print("Equation parsed successfully.")
except Exception as e:
    print(f"Error parsing equation: {e}")
    func = None

# Print parsed equation and x-range for confirmation
print(f"Parsed equation: y = {expr}")
print(f"x-range: {x_min} to {x_max}")

# Step 2: Generate data points for the plot
if func is not None:
    x_vals = np.linspace(x_min, x_max, 500)  # 500 points between x_min and x_max
    try:
        y_vals = func(x_vals)  # Calculate y values
        # If y_vals is a single value, make it an array
        if np.isscalar(y_vals):
            y_vals = np.full_like(x_vals, y_vals, dtype=float)
        print("First 5 x values:", x_vals[:5])
        print("First 5 y values:", y_vals[:5])

        plt.style.use('dark_background')  # Set dark background for plot
        fig, ax = plt.subplots()
        line, = ax.plot([], [], color='white', linewidth=2)  # Main plot line
        tip_marker, = ax.plot([], [], 'ro', markersize=6)  # Red dot at the tip
        tip_text = ax.text(0, 0, '', color='white', fontsize=10, ha='left', va='bottom', fontweight='bold')  # Text for tip

        # Prepare background axes (drawn as lines, not default spines)
        x_axis_bg, = ax.plot([], [], color='gray', linewidth=2, alpha=0.5, zorder=0)  # x=0 axis
        y_axis_bg, = ax.plot([], [], color='gray', linewidth=2, alpha=0.5, zorder=0)  # y=0 axis
        grid_lines = []
        for _ in range(20):  # Up to 10 grid lines each direction
            grid_lines.append(ax.plot([], [], color='gray', linewidth=0.5, alpha=0.2, zorder=0)[0])  # vertical
            grid_lines.append(ax.plot([], [], color='gray', linewidth=0.5, alpha=0.2, zorder=0)[0])  # horizontal

        # Hide axes, ticks, and spines for a clean look
        ax.set_axis_off()
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

        # Minimum window sizes for zooming effect
        min_x_window = (x_max - x_min) * 0.2 if (x_max - x_min) > 0 else 1
        y_range_total = np.max(y_vals) - np.min(y_vals)
        min_y_window = y_range_total * 0.2 if y_range_total > 0 else 1
        if min_y_window < 1e-6:
            min_y_window = 1

        # Check if the function is constant
        is_constant = np.allclose(y_vals, y_vals[0])
        constant_y = y_vals[0] if is_constant else None

        def init():
            # Initialize all plot elements as empty
            empty = np.array([])
            line.set_data(empty, empty)
            tip_marker.set_data(empty, empty)
            tip_text.set_text('')
            x_axis_bg.set_data(empty, empty)
            y_axis_bg.set_data(empty, empty)
            for gl in grid_lines:
                gl.set_data(empty, empty)
            return (line, tip_marker, tip_text, x_axis_bg, y_axis_bg, *grid_lines)

        def update(frame):
            # Update plot for each animation frame
            if frame == 0:
                empty = np.array([])
                line.set_data(empty, empty)
                tip_marker.set_data(empty, empty)
                tip_text.set_text('')
                x_axis_bg.set_data(empty, empty)
                y_axis_bg.set_data(empty, empty)
                for gl in grid_lines:
                    gl.set_data(empty, empty)
                return (line, tip_marker, tip_text, x_axis_bg, y_axis_bg, *grid_lines)
            x_data = np.array(x_vals[:frame])
            y_data = np.array(y_vals[:frame])
            line.set_data(x_data, y_data)
            tip_marker.set_data(np.array([x_vals[frame-1]]), np.array([y_vals[frame-1]]))
            tip_x = x_vals[frame-1]
            tip_y = y_vals[frame-1]
            # Show (x, y) at the tip
            tip_text.set_position((tip_x, tip_y))
            tip_text.set_text(f'({tip_x:.2f}, {tip_y:.2f})')
            # X window: zoom in around the tip
            x_window = max(min_x_window, (x_max - x_min) * 0.2)
            x_left = tip_x - x_window * 0.6
            x_right = tip_x + x_window * 0.4
            if x_left < x_min:
                x_left = x_min
                x_right = x_min + x_window
            if x_right > x_max:
                x_right = x_max
                x_left = x_max - x_window
            ax.set_xlim(x_left, x_right)
            # Y window: zoom in around the tip
            if is_constant:
                y_lower = constant_y - 1
                y_upper = constant_y + 1
            else:
                y_window = max(min_y_window, (np.max(y_vals[:frame]) - np.min(y_vals[:frame])) * 1.2)
                if y_window < 1e-6:
                    y_window = 1
                y_lower = tip_y - y_window * 0.5
                y_upper = tip_y + y_window * 0.5
                y_min_total = np.min(y_vals)
                y_max_total = np.max(y_vals)
                if y_lower < y_min_total:
                    y_lower = y_min_total
                    y_upper = y_min_total + y_window
                if y_upper > y_max_total:
                    y_upper = y_max_total
                    y_lower = y_max_total - y_window
                if y_lower == y_upper:
                    y_lower -= 1
                    y_upper += 1
            ax.set_ylim(y_lower, y_upper)
            # Draw background axes (cross at y=0 and x=0)
            x_axis_bg.set_data([x_left, x_right], [0, 0])
            y_axis_bg.set_data([0, 0], [y_lower, y_upper])
            # Draw grid lines
            n_grid = 10
            x_grid = np.linspace(x_left, x_right, n_grid)
            y_grid = np.linspace(y_lower, y_upper, n_grid)
            for i in range(n_grid):
                # vertical grid
                grid_lines[2*i].set_data([x_grid[i], x_grid[i]], [y_lower, y_upper])
                # horizontal grid
                grid_lines[2*i+1].set_data([x_left, x_right], [y_grid[i], y_grid[i]])
            return (line, tip_marker, tip_text, x_axis_bg, y_axis_bg, *grid_lines)

        # Create the animation
        ani = FuncAnimation(fig, update, frames=len(x_vals)+1, init_func=init, blit=False, interval=speed, repeat=False)
        plt.show()

        # Ask user if they want to save the animation
        save = input("Do you want to save the animation as a video? (y/n): ").strip().lower()
        if save == 'y':
            filename = input("Enter filename (without extension): ").strip()
            fmt = input("Enter format (mp4/gif): ").strip().lower()
            if fmt == 'mp4':
                try:
                    ani.save(f"{filename}.mp4", writer='ffmpeg', fps=50)
                    print(f"Animation saved as {filename}.mp4")
                except Exception as e:
                    print(f"Error saving MP4: {e}\nMake sure ffmpeg is installed.")
            elif fmt == 'gif':
                try:
                    ani.save(f"{filename}.gif", writer='pillow', fps=50)
                    print(f"Animation saved as {filename}.gif")
                except Exception as e:
                    print(f"Error saving GIF: {e}\nMake sure pillow is installed.")
            else:
                print("Unsupported format. Please use 'mp4' or 'gif'.")
    except Exception as e:
        print(f"Error evaluating function: {e}")