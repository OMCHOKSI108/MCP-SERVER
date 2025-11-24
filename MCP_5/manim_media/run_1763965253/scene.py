from manim import *
import numpy as np

class LogisticRegressionExplainer(Scene):
    def construct(self):
        # Title
        title = Text("Logistic Regression", font_size=48, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        # Create axes
        axes = Axes(
            x_range=[-6, 6, 1],
            y_range=[-0.2, 1.2, 0.2],
            x_length=8,
            y_length=4,
            axis_config={"color": BLUE, "include_numbers": True},
            tips=False,
        )
        axes.shift(DOWN * 0.3)
        
        # Labels
        x_label = axes.get_x_axis_label("x (feature)", edge=DOWN, direction=DOWN)
        y_label = axes.get_y_axis_label("P(y=1)", edge=LEFT, direction=LEFT)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(0.5)
        
        # Sigmoid function
        def sigmoid(x):
            return 1 / (1 + np.exp(-x))
        
        sigmoid_curve = axes.plot(
            sigmoid,
            x_range=[-6, 6],
            color=YELLOW,
            stroke_width=4
        )
        
        sigmoid_label = Text("σ(x) = 1/(1+e⁻ˣ)", font_size=28, color=YELLOW)
        sigmoid_label.next_to(sigmoid_curve, RIGHT, buff=0.3).shift(UP * 0.5)
        
        self.play(Create(sigmoid_curve), Write(sigmoid_label))
        self.wait(0.5)
        
        # Sample points for Class 0 (blue dots)
        class_0_x = [-4, -3.5, -3, -2.5, -2]
        class_0_points = VGroup(*[
            Dot(axes.c2p(x, 0), color=BLUE, radius=0.1)
            for x in class_0_x
        ])
        
        class_0_label = Text("Class 0", font_size=24, color=BLUE)
        class_0_label.next_to(axes.c2p(-3.5, 0), DOWN, buff=0.3)
        
        # Sample points for Class 1 (red dots)
        class_1_x = [2, 2.5, 3, 3.5, 4]
        class_1_points = VGroup(*[
            Dot(axes.c2p(x, 1), color=RED, radius=0.1)
            for x in class_1_x
        ])
        
        class_1_label = Text("Class 1", font_size=24, color=RED)
        class_1_label.next_to(axes.c2p(3.5, 1), UP, buff=0.3)
        
        self.play(
            FadeIn(class_0_points),
            Write(class_0_label)
        )
        self.wait(0.3)
        
        self.play(
            FadeIn(class_1_points),
            Write(class_1_label)
        )
        self.wait(0.5)
        
        # Decision boundary indicator
        decision_line = DashedLine(
            axes.c2p(0, -0.2),
            axes.c2p(0, 1.2),
            color=GREEN,
            stroke_width=3
        )
        decision_label = Text("Decision\nBoundary\n(x=0)", font_size=20, color=GREEN)
        decision_label.next_to(decision_line, RIGHT, buff=0.2)
        
        self.play(Create(decision_line), Write(decision_label))
        self.wait(0.5)
        
        # Key insight box
        insight_box = Rectangle(
            width=7,
            height=1.5,
            fill_color=DARK_GRAY,
            fill_opacity=0.8,
            stroke_color=WHITE,
            stroke_width=2
        )
        insight_box.to_edge(DOWN, buff=0.3)
        
        insight_text = VGroup(
            Text("Key Insight:", font_size=28, weight=BOLD, color=YELLOW),
            Text("Sigmoid maps any input to probability [0,1]", font_size=22)
        )
        insight_text.arrange(DOWN, buff=0.2)
        insight_text.move_to(insight_box.get_center())
        
        self.play(
            FadeIn(insight_box),
            Write(insight_text)
        )
        self.wait(2)
        
        # Fade out everything
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        self.wait(0.5)
