# 2D Equation Plotter & Animator

## Watch the demo
https://github.com/user-attachments/assets/85347c5c-0a7f-4d5a-a983-229109ea9fd3



## Overview
This Python application allows you to visualize and animate the plotting of 2D mathematical equations of the form `y = f(x)`. You can input any valid mathematical expression in terms of `x`, specify the range for `x`, and watch as the curve is drawn incrementally. The animation focuses on the tip of the curve, and you can export the animation as a video (MP4 or GIF). The interface is minimal, showing only the animated line, a moving tip marker, and the current (x, y) value at the tip.

---

## Features
- **Input any 2D equation** in terms of `x` (e.g., `sin(x) + x**2`, `exp(-x/10) * sin(5*x)`, etc.)
- **Customizable x-range** for plotting
- **Animated drawing** of the curve, with the focus following the tip
- **Minimalist display**: no axes, only the curve, tip marker, and current value
- **Tip marker** shows the current (x, y) value as the curve is drawn
- **Adjustable animation speed** (milliseconds per frame)
- **Export animation** as MP4 or GIF
- **Handles constant, oscillatory, and complex equations**

---

## Requirements
- Python 3.7+
- [NumPy](https://numpy.org/)
- [SymPy](https://www.sympy.org/)
- [Matplotlib](https://matplotlib.org/)
- For video export:
  - **MP4:** [ffmpeg](https://ffmpeg.org/) must be installed and available in your PATH
  - **GIF:** [pillow](https://python-pillow.org/) (PIL) must be installed

Install requirements with:
```bash
pip install numpy sympy matplotlib pillow
```

---

## Installation
1. Clone or download this repository.
2. Ensure you have the required Python packages (see above).
3. (Optional) Install `ffmpeg` for MP4 export:
   - On macOS: `brew install ffmpeg`
   - On Ubuntu: `sudo apt install ffmpeg`
   - On Windows: [Download from ffmpeg.org](https://ffmpeg.org/download.html)

---

## Usage
Run the script from your terminal:
```bash
python plot_2d_equations_input.py
```

### Step-by-Step Interaction
1. **Set Animation Speed:**
   - Enter the speed in milliseconds per frame (e.g., `20` for default, `10` for faster, `50` for slower).
2. **Enter Equation:**
   - Input the right-hand side of your equation for `y` in terms of `x` (e.g., `sin(x) + x**2`).
3. **Enter x-range:**
   - Specify the minimum and maximum values for `x` (e.g., `-10` and `10`).
4. **Watch the Animation:**
   - The curve will be drawn incrementally, with the tip and its (x, y) value shown.
5. **Export Animation (Optional):**
   - After the animation, you will be prompted to save the animation as a video (MP4 or GIF).

### Example Equations to Try
- `sin(x) * x**2`
- `cos(x) * exp(-0.1*x) * x`
- `log(abs(x)) * sin(2*x)`
- `x**3 - 6*x**2 + 4*x + 12`
- `sin(x) + sin(2*x)/2 + sin(3*x)/3`
- `exp(sin(x)) - cos(2*x)`
- `sin(x**2)`
- `abs(sin(x)) * x`

### Example Session
```
Enter animation speed (milliseconds per frame, default 20): 15
Enter the equation for y in terms of x (e.g., sin(x) + x**2):
y = sin(x) + x**2
Enter the x-range for plotting:
x min: -5
x max: 5
```

---

## Animation & Video Export
- After the animation, you can save the result as an MP4 or GIF.
- For MP4, ensure `ffmpeg` is installed.
- For GIF, ensure `pillow` is installed.
- The script will prompt for filename and format.

---

## Customization
- **Animation Speed:** Set at the start (ms per frame).
- **Appearance:**
  - Black background, white curve, red tip marker
  - No axes or grid for a clean look
  - Tip value displayed at the moving tip
- **Equation Complexity:** Supports any valid NumPy/SymPy expression in `x`.

---

## Troubleshooting
- **No line appears:**
  - Check your equation and x-range for valid values.
  - For constant equations, the line will be horizontal.
- **Export fails:**
  - For MP4, ensure `ffmpeg` is installed and in your PATH.
  - For GIF, ensure `pillow` is installed.
- **Equation errors:**
  - Ensure your equation is valid Python math syntax and uses `x` as the variable.
- **Animation too fast/slow:**
  - Adjust the speed parameter at the start.

---

## Credits
- Developed using Python, NumPy, SymPy, and Matplotlib.
- Animation export powered by Matplotlib's `FuncAnimation`.

---

## License
This project is open source and free to use for educational and personal purposes.
