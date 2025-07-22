import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
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

        plt.style.use('dark_background')
        fig, ax = plt.subplots()
        line, = ax.plot([], [], color='white', linewidth=2)
        tip_marker, = ax.plot([], [], 'ro', markersize=6)
        tip_text = ax.text(0, 0, '', color='white', fontsize=10, ha='left', va='bottom', fontweight='bold')

        # Prepare background axes (as lines, not spines)
        x_axis_bg, = ax.plot([], [], color='gray', linewidth=1, alpha=0.3, zorder=0)
        y_axis_bg, = ax.plot([], [], color='gray', linewidth=1, alpha=0.3, zorder=0)

        # Hide axes, ticks, and spines
        ax.set_axis_off()
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

        # Minimum window sizes
        min_x_window = (x_max - x_min) * 0.2 if (x_max - x_min) > 0 else 1
        y_range_total = np.max(y_vals) - np.min(y_vals)
        min_y_window = y_range_total * 0.2 if y_range_total > 0 else 1
        if min_y_window < 1e-6:
            min_y_window = 1

        is_constant = np.allclose(y_vals, y_vals[0])
        constant_y = y_vals[0] if is_constant else None

        def init():
            empty = np.array([])
            line.set_data(empty, empty)
            tip_marker.set_data(empty, empty)
            tip_text.set_text('')
            x_axis_bg.set_data(empty, empty)
            y_axis_bg.set_data(empty, empty)
            return line, tip_marker, tip_text, x_axis_bg, y_axis_bg

        def update(frame):
            if frame == 0:
                empty = np.array([])
                line.set_data(empty, empty)
                tip_marker.set_data(empty, empty)
                tip_text.set_text('')
                x_axis_bg.set_data(empty, empty)
                y_axis_bg.set_data(empty, empty)
                return line, tip_marker, tip_text, x_axis_bg, y_axis_bg
            x_data = np.array(x_vals[:frame])
            y_data = np.array(y_vals[:frame])
            line.set_data(x_data, y_data)
            tip_marker.set_data(np.array([x_vals[frame-1]]), np.array([y_vals[frame-1]]))
            tip_x = x_vals[frame-1]
            tip_y = y_vals[frame-1]
            # Show (x, y) at the tip
            tip_text.set_position((tip_x, tip_y))
            tip_text.set_text(f'({tip_x:.2f}, {tip_y:.2f})')
            # X window
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
            # Y window
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
            return line, tip_marker, tip_text, x_axis_bg, y_axis_bg

        ani = FuncAnimation(fig, update, frames=len(x_vals)+1, init_func=init, blit=False, interval=speed, repeat=False)
        plt.show()

        # Prompt to save animation
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