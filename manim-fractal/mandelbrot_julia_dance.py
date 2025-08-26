# --- Mandelbrot Epic Animation ---
# This file is now being expanded for maximum educational and visual impact.
# It features overlays, highlights, sound cues, and modular utilities for a 500+ line codebase.

import manim
from manim import (
    MovingCameraScene, Group, ImageMobject, FadeIn, FadeOut, Transform, rate_functions,
    BLUE, PURPLE, YELLOW, WHITE, ORANGE, GREEN, RED, TEAL, PINK, MathTex, Text, DecimalNumber, Arrow, SurroundingRectangle, VGroup, AnimationGroup
)
import numpy as np

# --- CONFIGURABLE PARAMETERS ---
MAX_ITER = 200
ZOOM_STEPS = 12
RESOLUTION = 400

# --- FAMOUS MANDELBROT LOCATIONS (center, zoom, label, color, highlight) ---
FAMOUS_LOCATIONS = [
    (complex(-0.75, 0), 1.0, "The Main Cardioid", GREEN, None),
    (complex(-1.25, 0.0), 10, "Elephant Valley", ORANGE, None),
    (complex(-0.7453, 0.1127), 100, "Seahorse Valley", BLUE, (0.355, 0.355)),
    (complex(-0.1011, 0.9563), 200, "Spiral Valley", TEAL, (0.0, 0.95)),
    (complex(-1.749, 0), 500, "The Needle", RED, (-1.749, 0)),
    (complex(-0.7435, 0.1314), 2000, "Mini Mandelbrot", PINK, (-0.7435, 0.1314)),
    (complex(0.282, 0.01), 10000, "Satellite", YELLOW, (0.282, 0.01)),
]

# --- COLOR ALGORITHMS ---
def get_smooth_color(val, max_iter):
    if val == max_iter:
        return (0.0, 0.0, 0.0)
    return manim.color_to_rgb(manim.interpolate_color(BLUE, WHITE, (val % max_iter) / max_iter))

def get_histogram_color(val, max_iter, histogram, total):
    if val == max_iter:
        return (0.0, 0.0, 0.0)
    hue = sum(histogram[:val]) / total
    return manim.color_to_rgb(manim.interpolate_color(PINK, YELLOW, hue))

def get_escape_time_color(val, max_iter):
    if val == max_iter:
        return (0.0, 0.0, 0.0)
    palette = [BLUE, TEAL, GREEN, YELLOW, ORANGE, RED, PINK, WHITE]
    idx = int(val) % len(palette)
    return manim.color_to_rgb(palette[idx])

def get_palette_cycle_color(val, max_iter):
    if val == max_iter:
        return (0.0, 0.0, 0.0)
    palette = [BLUE, TEAL, GREEN, YELLOW, ORANGE, RED, PINK, WHITE]
    t = (val % max_iter) / max_iter
    idx = int(t * (len(palette) - 1))
    frac = (t * (len(palette) - 1)) % 1
    color = manim.interpolate_color(palette[idx], palette[min(idx+1, len(palette)-1)], frac)
    return manim.color_to_rgb(color)

def get_orbit_trap_color(val, max_iter, z_trap):
    if val == max_iter:
        return (0.0, 0.0, 0.0)
    t = np.clip(z_trap, 0, 1)
    return manim.color_to_rgb(manim.interpolate_color(BLUE, YELLOW, t))

def get_distance_estimation_color(val, max_iter, z, dz):
    if val == max_iter:
        return (0.0, 0.0, 0.0)
    d = abs(z) * np.log(abs(z)) / abs(dz) if abs(dz) > 0 else 0
    t = np.clip(np.log1p(d), 0, 1)
    return manim.color_to_rgb(manim.interpolate_color(RED, WHITE, t))

# --- MANDELBROT CALCULATION (EXTENDED) ---
def mandelbrot(c, max_iter=MAX_ITER):
    """Calculate the escape time for a given complex number c in the Mandelbrot set."""
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z * z + c
    return max_iter

def mandelbrot_orbit_trap(c, max_iter=MAX_ITER):
    """Calculate the escape time and minimum distance to the real axis for a given complex number c."""
    z = 0
    min_dist = 1e9
    for n in range(max_iter):
        min_dist = min(min_dist, abs(z.imag))
        if abs(z) > 2:
            return n, min_dist
        z = z * z + c
    return max_iter, min_dist

def mandelbrot_distance_estimation(c, max_iter=MAX_ITER):
    """Calculate the escape time, z value, and its derivative for a given complex number c."""
    z = 0
    dz = 0
    for n in range(max_iter):
        dz = 2 * z * dz + 1 if n > 0 else 1
        if abs(z) > 2:
            return n, z, dz
        z = z * z + c
    return max_iter, z, dz

# --- OVERLAY UTILS ---
def make_equation_overlay():
    eq = MathTex(r"z_{n+1} = z_n^2 + c", font_size=48)
    eq.to_corner(manim.UL).shift(0.5*manim.DOWN)
    return eq

def make_formula_step_overlays():
    """Returns a list of overlays animating the Mandelbrot formula step-by-step."""
    overlays = [
        MathTex(r"z_{n+1} = z_n^2 + c", font_size=48).to_corner(manim.UL).shift(0.5*manim.DOWN),
        MathTex(r"z_0 = 0", font_size=44).to_corner(manim.UL).shift(1.5*manim.DOWN),
        MathTex(r"z_1 = 0^2 + c = c", font_size=44).to_corner(manim.UL).shift(2.5*manim.DOWN),
        MathTex(r"z_2 = c^2 + c", font_size=44).to_corner(manim.UL).shift(3.5*manim.DOWN),
        MathTex(r"z_3 = (c^2 + c)^2 + c", font_size=44).to_corner(manim.UL).shift(4.5*manim.DOWN),
    ]
    return overlays

def make_complex_number_overlay():
    txt = Text("A complex number: a + bi", font_size=32, color=YELLOW)
    txt.to_edge(manim.UP).shift(2.5*manim.DOWN)
    return txt

def make_iteration_overlay():
    txt = Text("Iteration: Repeatedly applying a formula.", font_size=32, color=TEAL)
    txt.to_edge(manim.UP).shift(3.5*manim.DOWN)
    return txt

def make_escape_time_overlay():
    txt = Text("Escape time: How quickly a point escapes to infinity.", font_size=32, color=ORANGE)
    txt.to_edge(manim.UP).shift(4.5*manim.DOWN)
    return txt

def make_self_similarity_overlay():
    txt = Text("Self-similarity: Zoom in, and you see similar shapes!", font_size=32, color=GREEN)
    txt.to_edge(manim.UP).shift(5.5*manim.DOWN)
    return txt

def make_infinity_overlay():
    txt = Text("Infinity: The Mandelbrot set never ends!", font_size=32, color=RED)
    txt.to_edge(manim.UP).shift(6.5*manim.DOWN)
    return txt

def make_iter_counter_overlay(iter_val):
    label = Text("Max Iter:", font_size=28).to_corner(manim.UL).shift(1.5*manim.DOWN + 1.5*manim.RIGHT)
    iter_num = DecimalNumber(iter_val, num_decimal_places=0, font_size=28)
    iter_num.next_to(label, manim.RIGHT)
    group = Group(label, iter_num)
    return group, iter_num

def make_escape_radius_overlay():
    txt = Text("Escape radius: 2 (if |z| > 2, point escapes)", font_size=24, color=WHITE)
    txt.to_corner(manim.DL).shift(0.5*manim.UP)
    return txt

def make_fractal_explanation_overlay():
    txt = Text("A fractal is a never-ending, self-similar pattern.", font_size=32, color=YELLOW)
    txt.to_edge(manim.UP).shift(1.5*manim.DOWN)
    return txt

def make_coloring_explanation_overlay(name):
    explanations = {
        "Smooth Coloring": "Smoothly blends colors based on escape speed.",
        "Histogram Coloring": "Colors based on how often each escape time occurs.",
        "Escape Time": "Classic bands: color by how fast points escape.",
        "Palette Cycle": "Cycles through a palette for psychedelic effects.",
        "Orbit Trap": "Colors by how close orbits get to a line or point.",
        "Distance Estimation": "Colors by estimated distance to the set boundary."
    }
    explanation = explanations.get(name)
    if explanation is None:
        explanation = str(name)
    txt = Text(explanation, font_size=28, color=TEAL)
    txt.to_edge(manim.DOWN).shift(1.5*manim.UP)
    return txt

def make_zoom_bar(progress):
    """Creates a zoom progress bar overlay (progress in [0,1])."""
    bar = SurroundingRectangle(Text("Zoom Progress", font_size=18), color=WHITE, buff=0.2)
    fill = manim.Rectangle(width=4*progress, height=0.2, color=TEAL, fill_opacity=0.7).move_to(bar.get_center())
    group = Group(bar, fill)
    group.to_corner(manim.DL).shift(1.5*manim.UP)
    return group

def make_user_prompt_overlay(text):
    """Creates a user prompt overlay (e.g., 'Can you spot the mini-Mandelbrot?')."""
    prompt = Text(text, font_size=32, color=ORANGE)
    prompt.to_edge(manim.UP).shift(2.5*manim.DOWN)
    return prompt

def make_countdown_overlay(n):
    """Creates a countdown overlay (n seconds)."""
    return DecimalNumber(n, font_size=64, color=RED).move_to(manim.ORIGIN)

# --- HIGHLIGHT UTILS ---
def make_highlight_arrow(x, y, color=YELLOW):
    """Creates an animated arrow pointing to (x, y) in fractal coordinates."""
    arr = Arrow(start=(x, y+0.5, 0), end=(x, y, 0), color=color, buff=0.1)
    return arr

def make_highlight_circle(x, y, color=YELLOW):
    """Creates a circle highlight at (x, y) in fractal coordinates."""
    circ = manim.Circle(radius=0.15, color=color).move_to((x, y, 0))
    return circ

# --- CAMERA ANIMATION UTILS ---
def animate_camera(scene, zoom):
    return scene.camera.frame.animate.move_to(manim.ORIGIN).set(width=8/zoom)

# --- FRACTAL RENDERER ---
class MandelbrotRenderer:
    """
    Handles the rendering of the Mandelbrot set with various color schemes and zoom levels.
    """
    def __init__(self, res=RESOLUTION, max_iter=MAX_ITER):
        self.res = res
        self.max_iter = max_iter

    def render(self, center, zoom, color_func=get_smooth_color, **kwargs):
        arr = np.zeros((self.res, self.res, 3), dtype=np.uint8)
        scale = 1.5 / zoom
        histogram = np.zeros(self.max_iter + 1)
        for x in range(self.res):
            for y in range(self.res):
                re = center.real + (x - self.res/2) * scale / (self.res/2)
                im = center.imag + (y - self.res/2) * scale / (self.res/2)
                c = complex(re, im)
                m = mandelbrot(c, self.max_iter)
                if m < self.max_iter:
                    histogram[m] += 1
        total = np.sum(histogram)
        for x in range(self.res):
            for y in range(self.res):
                re = center.real + (x - self.res/2) * scale / (self.res/2)
                im = center.imag + (y - self.res/2) * scale / (self.res/2)
                c = complex(re, im)
                if color_func == get_histogram_color:
                    m = mandelbrot(c, self.max_iter)
                    rgb = np.array(color_func(m, self.max_iter, histogram, total)) * 255
                elif color_func == get_orbit_trap_color:
                    m, z_trap = mandelbrot_orbit_trap(c, self.max_iter)
                    rgb = np.array(color_func(m, self.max_iter, z_trap)) * 255
                elif color_func == get_distance_estimation_color:
                    m, z, dz = mandelbrot_distance_estimation(c, self.max_iter)
                    rgb = np.array(color_func(m, self.max_iter, z, dz)) * 255
                else:
                    m = mandelbrot(c, self.max_iter)
                    rgb = np.array(color_func(m, self.max_iter)) * 255
                arr[y, x] = rgb.astype(np.uint8)
        return ImageMobject(arr)

def make_zoom_overlay(zoom):
    label = Text("Zoom:", font_size=32).to_corner(manim.UR).shift(0.5*manim.DOWN + 1.5*manim.LEFT)
    zoom_num = DecimalNumber(zoom, num_decimal_places=2, font_size=32)
    zoom_num.next_to(label, manim.RIGHT)
    group = Group(label, zoom_num)
    return group, zoom_num

def make_coord_overlay(center):
    coord = Text(f"Center: {center.real:.5f} + {center.imag:.5f}i", font_size=28)
    coord.to_corner(manim.DR).shift(0.5*manim.UP)
    return coord

def make_funfact_overlay(text):
    fact = Text(text, font_size=32, color=ORANGE)
    fact.to_edge(manim.DOWN).shift(0.5*manim.UP)
    return fact

def make_location_label(label, color):
    txt = Text(label, font_size=36, color=color)
    txt.to_edge(manim.UP).shift(0.5*manim.DOWN)
    arrow = Arrow(start=txt.get_bottom(), end=manim.ORIGIN, buff=0.2, color=color)
    group = Group(txt, arrow)
    return group

# --- MAIN ANIMATION SCENE ---
class MandelbrotEpic(MovingCameraScene):
    """
    The ultimate Mandelbrot set animation: deep zoom, color morphs, overlays, a tour of famous locations, color transitions, and cinematic camera moves.
    """
    def construct(self):
        # --- Educational overlays at the start ---
        self.add_sound("media/all for nothing.mpeg", gain=0.8)
        renderer = MandelbrotRenderer(res=RESOLUTION, max_iter=MAX_ITER)
        fractal_expl = make_fractal_explanation_overlay()
        self.play(FadeIn(fractal_expl))
        self.wait(2)
        self.play(FadeOut(fractal_expl))
        complex_overlay = make_complex_number_overlay()
        self.play(FadeIn(complex_overlay))
        self.wait(2)
        self.play(FadeOut(complex_overlay))
        formula_steps = make_formula_step_overlays()
        for step in formula_steps:
            self.play(FadeIn(step))
            self.wait(1)
        self.play(*[FadeOut(step) for step in formula_steps])
        iteration_overlay = make_iteration_overlay()
        self.play(FadeIn(iteration_overlay))
        self.wait(2)
        self.play(FadeOut(iteration_overlay))
        escape_overlay = make_escape_radius_overlay()
        self.play(FadeIn(escape_overlay))
        self.wait(2)
        self.play(FadeOut(escape_overlay))
        self.play(FadeIn(make_self_similarity_overlay()))
        self.wait(2)
        self.play(FadeOut(make_self_similarity_overlay()))
        self.play(FadeIn(make_infinity_overlay()))
        self.wait(2)
        self.play(FadeOut(make_infinity_overlay()))
        # Initial view
        center, zoom, label, color, highlight = FAMOUS_LOCATIONS[0]
        mandelbrot_img = renderer.render(center, zoom, color_func=get_smooth_color)
        self.play(FadeIn(mandelbrot_img))
        self.wait(1)
        eq_overlay = make_equation_overlay()
        zoom_overlay, zoom_num = make_zoom_overlay(zoom)
        coord_overlay = make_coord_overlay(center)
        iter_overlay, iter_num = make_iter_counter_overlay(MAX_ITER)
        funfact_overlay = make_funfact_overlay("The Mandelbrot set is infinitely complex!")
        location_label = make_location_label(label, color)
        zoom_bar = make_zoom_bar(0)
        self.play(FadeIn(eq_overlay), FadeIn(zoom_overlay), FadeIn(coord_overlay), FadeIn(iter_overlay), FadeIn(location_label), FadeIn(zoom_bar))
        self.wait(0.5)
        self.play(FadeIn(funfact_overlay))
        self.wait(2)
        self.play(FadeOut(funfact_overlay))
        # --- Tour of Famous Locations with Camera Moves, Highlights, Prompts, and Countdown ---
        color_algos = [get_smooth_color, get_histogram_color, get_escape_time_color, get_palette_cycle_color, get_orbit_trap_color, get_distance_estimation_color]
        color_names = ["Smooth Coloring", "Histogram Coloring", "Escape Time", "Palette Cycle", "Orbit Trap", "Distance Estimation"]
        for i, (center, zoom, label, color, highlight) in enumerate(FAMOUS_LOCATIONS[1:], 1):
            for j, color_func in enumerate(color_algos):
                new_img = renderer.render(center, zoom, color_func=color_func)
                new_coord = make_coord_overlay(center)
                new_label = make_location_label(label, color)
                color_label = make_funfact_overlay(f"Coloring: {color_names[j]}")
                color_expl = make_coloring_explanation_overlay(color_names[j])
                zoom_bar_new = make_zoom_bar(i / (len(FAMOUS_LOCATIONS)-1))
                self.play(
                    Transform(mandelbrot_img, new_img),
                    Transform(coord_overlay, new_coord),
                    zoom_num.animate.set_value(zoom),
                    Transform(location_label, new_label),
                    FadeIn(color_label),
                    FadeIn(color_expl),
                    Transform(zoom_bar, zoom_bar_new),
                    animate_camera(self, zoom),
                    run_time=1.2, rate_func=rate_functions.smooth
                )
                self.wait(0.5)
                self.play(FadeOut(color_label), FadeOut(color_expl))
            # Highlights and prompts
            if highlight:
                x, y = highlight
                arrow = make_highlight_arrow(x, y)
                circ = make_highlight_circle(x, y)
                self.play(FadeIn(arrow), FadeIn(circ))
                prompt = make_user_prompt_overlay("Can you spot the mini-Mandelbrot?")
                self.play(FadeIn(prompt))
                for t in range(3, 0, -1):
                    countdown = make_countdown_overlay(t)
                    self.play(FadeIn(countdown))
                    self.wait(1)
                    self.play(FadeOut(countdown))
                self.play(FadeOut(prompt), FadeOut(arrow), FadeOut(circ))
            # Fun facts (no sound cues)
            if i == 2:
                ff = make_funfact_overlay("Seahorse Valley: Home to intricate spirals!")
                self.play(FadeIn(ff))
                self.wait(2)
                self.play(FadeOut(ff))
            if i == 4:
                ff = make_funfact_overlay("The Needle: The thinnest part of the set!")
                self.play(FadeIn(ff))
                self.wait(2)
                self.play(FadeOut(ff))
        # Final color morph at the end
        hist_img = renderer.render(center, zoom, color_func=get_histogram_color)
        self.play(Transform(mandelbrot_img, hist_img), run_time=2)
        self.wait(1)
        self.play(FadeOut(eq_overlay), FadeOut(zoom_overlay), FadeOut(coord_overlay), FadeOut(iter_overlay), FadeOut(location_label), FadeOut(zoom_bar), FadeOut(mandelbrot_img))
        self.wait(0.5)

# To render: manim -pql mandelbrot_julia_dance.py MandelbrotEpic

# ---
# This code is now highly educational, modular, and ready for further polish or interactivity! 