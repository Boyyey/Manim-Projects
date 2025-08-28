from manim import *

class PythagoreanTheorem(Scene):
    def construct(self):
        # Triangle points
        A = ORIGIN
        B = A + 4*RIGHT
        C = A + 3*UP

        # Triangle
        triangle = Polygon(A, B, C, color=BLUE)
        triangle_label = MathTex("a", "b", "c")
        triangle_label[0].next_to(Line(B, A).get_center(), DOWN)
        triangle_label[1].next_to(Line(C, A).get_center(), LEFT)
        triangle_label[2].next_to(Line(C, B).get_center(), UP)

        self.play(Create(triangle), Write(triangle_label))
        self.wait(1)

        # Square on side a (vertical)
        square_a = Square(side_length=3, fill_opacity=0.5, fill_color=YELLOW)
        square_a.move_to(Line(C, A).get_center() + LEFT*1.5)

        # Square on side b (horizontal)
        square_b = Square(side_length=4, fill_opacity=0.5, fill_color=GREEN)
        square_b.move_to(Line(B, A).get_center() + DOWN*2)

        # Square on hypotenuse (diagonal)
        hypotenuse = Line(C, B)
        square_c = Square(side_length=hypotenuse.get_length(), fill_opacity=0.5, fill_color=RED)
        square_c.rotate(hypotenuse.get_angle())
        square_c.move_to(hypotenuse.get_center() + RIGHT*0.5 + UP*0.5)

        # Show squares
        self.play(FadeIn(square_a), FadeIn(square_b))
        self.wait(1)
        self.play(FadeIn(square_c))
        self.wait(1)

        # Equation
        equation = MathTex("a^2 + b^2 = c^2").to_edge(DOWN)
        self.play(Write(equation))
        self.wait(2)
