from manim import *
import numpy as np

class MLClassification(Scene):
    def construct(self):
        # Title
        title = Text("Logistic Regression & KNN", font_size=40)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP))
        
        # Logistic Regression Section
        lr_title = Text("Logistic Regression", font_size=32, color=BLUE)
        lr_title.shift(UP * 2)
        self.play(FadeIn(lr_title))
        
        # Sigmoid formula
        formula = MathTex(r"\sigma(x) = \frac{1}{1 + e^{-x}}", font_size=36)
        formula.next_to(lr_title, DOWN)
        self.play(Write(formula))
        self.wait()
        
        # Axes
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[0, 1, 0.5],
            x_length=6,
            y_length=3,
            axis_config={"include_tip": False}
        )
        axes.shift(DOWN)
        self.play(FadeOut(formula), Create(axes))
        
        # Sigmoid curve
        sigmoid = axes.plot(lambda x: 1/(1+np.exp(-x)), color=YELLOW, stroke_width=3)
        self.play(Create(sigmoid), run_time=2)
        
        # Decision boundary
        boundary = DashedLine(axes.c2p(-5, 0.5), axes.c2p(5, 0.5), color=RED)
        self.play(Create(boundary))
        
        # Labels
        c0 = Text("Class 0", font_size=20, color=BLUE).next_to(axes.c2p(-3, 0.1), DOWN)
        c1 = Text("Class 1", font_size=20, color=GREEN).next_to(axes.c2p(3, 0.9), UP)
        self.play(FadeIn(c0), FadeIn(c1))
        self.wait(2)
        
        # Clear
        self.play(*[FadeOut(m) for m in [axes, sigmoid, boundary, c0, c1, lr_title]])
        
        # KNN Section
        knn_title = Text("K-Nearest Neighbors", font_size=32, color=PURPLE)
        knn_title.shift(UP * 2.5)
        self.play(Write(knn_title))
        
        # 2D plane
        plane = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=5,
            y_length=5,
            axis_config={"include_tip": False}
        )
        self.play(Create(plane))
        
        # Data points
        blues = [(-2,-1), (-1.5,-2), (-1,-0.5)]
        greens = [(1.5,1.5), (2,2), (1,2)]
        
        blue_dots = VGroup(*[Dot(plane.c2p(x,y), color=BLUE) for x,y in blues])
        green_dots = VGroup(*[Dot(plane.c2p(x,y), color=GREEN) for x,y in greens])
        
        self.play(Create(blue_dots), Create(green_dots))
        
        # Test point
        test = Dot(plane.c2p(0, 0.5), color=YELLOW, radius=0.12)
        label = Text("?", font_size=28, color=YELLOW).next_to(test, UP)
        self.play(GrowFromCenter(test), Write(label))
        self.wait()
        
        # K=3
        k_label = Text("K=3", font_size=24).to_corner(UL)
        self.play(Write(k_label))
        
        # Lines to neighbors
        lines = VGroup(
            Line(plane.c2p(0,0.5), plane.c2p(1,2), color=GREEN),
            Line(plane.c2p(0,0.5), plane.c2p(1.5,1.5), color=GREEN),
            Line(plane.c2p(0,0.5), plane.c2p(-1,-0.5), color=BLUE)
        )
        self.play(Create(lines))
        
        result = Text("→ Class 1", font_size=24, color=GREEN).next_to(k_label, DOWN)
        self.play(Write(result))
        self.play(test.animate.set_color(GREEN))
        self.wait(2)
        
        self.play(*[FadeOut(m) for m in self.mobjects])