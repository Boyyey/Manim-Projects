# 🌀 Mandelbrot & Julia: The Dance of Infinity

Dive into the mesmerizing world of fractals! This project animates a deep zoom into the Mandelbrot set, then morphs into related Julia sets, showing how changing the complex parameter `c` transforms the Julia set's shape. Experience stunning color maps, organic transitions, and the hypnotic dance of infinity.

## ✨ Features
- Ultra-smooth deep zoom into the Mandelbrot set
- Dynamic, organic transitions to Julia sets
- Animated morphing of Julia sets as `c` changes
- Beautiful, customizable color maps
- Optimized for performance (suitable for deep zooms)

## 🚀 Quick Start

1. **Install [Manim](https://docs.manim.community/en/stable/):**
   ```bash
   pip install manim
   ```
2. **Run the Animation:**
   ```bash
   manim -pql mandelbrot_julia_dance.py MandelbrotJuliaDance
   ```
   - `-pql` means: Preview, Quick, Low quality (for fast rendering). For higher quality, use `-pqh` or `-pqh`.

3. **Enjoy the fractal dance!**

## 📝 Description
This animation starts with a deep zoom into the iconic Mandelbrot set, then smoothly transitions to a Julia set whose parameter `c` is chosen from the zoomed Mandelbrot region. The Julia set then morphs as `c` animates in a circle, revealing the infinite variety of fractal shapes.

## 📂 Files
- `mandelbrot_julia_dance.py` — The Manim animation script
- `README.md` — This file

## 💡 Tips
- Tweak `MAX_ITER`, `ZOOM_STEPS`, and `JULIA_STEPS` in the script for different effects or performance.
- Try different color maps for unique visuals!

---
Made with ❤️ and 🧠 using [Manim](https://www.manim.community/) 