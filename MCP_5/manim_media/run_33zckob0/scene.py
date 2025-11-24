from manim import *
import numpy as np

class LogisticRegressionExplainer(Scene):
    def construct(self):
        # Title
        title = Text("Logistic Regression", font_size=48, color=BLUE)
        self.play(Write(title))
        self.wait()
        self.play(title.animate.to_edge(UP))
        
        # Create axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-0.2, 1.2, 0.2],
            x_length=8,
            y_length=4,
            axis_config={"color": WHITE},
            tips=False
        )
        
        x_label = Text("x", font_size=24)
        x_label.next_to(axes.x_axis, DOWN)
        y_label = Text("P(y=1)", font_size=24)
        y_label.next_to(axes.y_axis, LEFT).shift(UP)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait()
        
        # Sigmoid function
        sigmoid = axes.plot(
            lambda x: 1 / (1 + np.exp(-x)),
            color=YELLOW,
            x_range=[-3, 3]
        )
        
        sigmoid_label = Text("Sigmoid: 1/(1+e^-x)", font_size=30, color=YELLOW)
        sigmoid_label.next_to(axes, RIGHT).shift(UP)
        
        self.play(Create(sigmoid), Write(sigmoid_label))
        self.wait()
        
        # Show threshold at 0.5
        threshold_line = DashedLine(
            axes.c2p(-3, 0.5),
            axes.c2p(3, 0.5),
            color=RED
        )
        threshold_label = Text("Decision Threshold = 0.5", font_size=24, color=RED)
        threshold_label.next_to(threshold_line, RIGHT)
        
        self.play(Create(threshold_line), Write(threshold_label))
        self.wait()
        
        # Add sample points
        class_0_points = VGroup(*[
            Dot(axes.c2p(x, 0.1), color=BLUE) 
            for x in [-2.5, -2, -1.5, -1]
        ])
        class_1_points = VGroup(*[
            Dot(axes.c2p(x, 0.9), color=GREEN) 
            for x in [1, 1.5, 2, 2.5]
        ])
        
        class_0_label = Text("Class 0", font_size=24, color=BLUE).next_to(class_0_points, LEFT)
        class_1_label = Text("Class 1", font_size=24, color=GREEN).next_to(class_1_points, RIGHT)
        
        self.play(
            FadeIn(class_0_points),
            FadeIn(class_1_points),
            Write(class_0_label),
            Write(class_1_label)
        )
        self.wait()
        
        # Key insight box
        insight = VGroup(
            Rectangle(width=6, height=1.5, color=PURPLE, fill_opacity=0.2),
            Text("Key: Maps input to probability [0,1]", font_size=28, color=WHITE)
        ).arrange(DOWN, buff=0.2)
        insight.to_corner(DL)
        
        self.play(FadeIn(insight))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
