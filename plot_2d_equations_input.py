import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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

        # Improved animation with minimum window size and tip at 60% of x-axis
        plt.style.use('dark_background')
        fig, ax = plt.subplots()
        line, = ax.plot([], [], color='white', linewidth=2)
        tip_marker, = ax.plot([], [], 'ro', markersize=6)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(f'y = {equation_str}')

        # Minimum window sizes
        min_x_window = (x_max - x_min) * 0.2 if (x_max - x_min) > 0 else 1
        y_range_total = np.max(y_vals) - np.min(y_vals)
        min_y_window = y_range_total * 0.2 if y_range_total > 0 else 1
        if min_y_window < 1e-6:
            min_y_window = 1  # Sensible default for constant or nearly constant functions

        is_constant = np.allclose(y_vals, y_vals[0])
        constant_y = y_vals[0] if is_constant else None

        def init():
            empty = np.array([])
            line.set_data(empty, empty)
            tip_marker.set_data(empty, empty)
            print(f"[init] line: {type(empty)}, shape: {empty.shape}")
            return line, tip_marker

        def update(frame):
            if frame == 0:
                empty = np.array([])
                line.set_data(empty, empty)
                tip_marker.set_data(empty, empty)
                print(f"[update frame 0] line: {type(empty)}, shape: {empty.shape}")
                return line, tip_marker
            x_data = np.array(x_vals[:frame])
            y_data = np.array(y_vals[:frame])
            line.set_data(x_data, y_data)
            print(f"[update frame {frame}] line: {type(x_data)}, shape: {x_data.shape}")
            if frame > 0:
                tip_marker.set_data(np.array([x_vals[frame-1]]), np.array([y_vals[frame-1]]))
                print(f"[update frame {frame}] tip: {type(np.array([x_vals[frame-1]]))}, shape: {np.array([x_vals[frame-1]]).shape}")
            else:
                tip_marker.set_data(np.array([]), np.array([]))
            tip_x = x_vals[frame-1]
            tip_y = y_vals[frame-1]
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
            # Debug prints for axis limits
            print(f"Frame {frame}: xlim=({x_left:.2f}, {x_right:.2f}), ylim=({y_lower:.2f}, {y_upper:.2f})")
            return line, tip_marker

        ani = FuncAnimation(fig, update, frames=len(x_vals)+1, init_func=init, blit=True, interval=20, repeat=False)
        plt.show()
    except Exception as e:
        print(f"Error evaluating function: {e}")