from manim import *

class CNNExplainer(Scene):
    def construct(self):
        # Title
        title = Text("CNN Architecture", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.3)
        
        # Input Image
        input_text = Text("Input\nImage", font_size=20).shift(LEFT*5 + UP)
        input_box = Square(1.2, fill_opacity=0.3, fill_color=BLUE).next_to(input_text, DOWN)
        self.play(FadeIn(input_text), Create(input_box))
        self.wait(0.3)
        
        # Convolution
        conv_text = Text("Conv\n3×3", font_size=18).shift(LEFT*2.5 + UP)
        conv_boxes = VGroup(*[
            Rectangle(height=1, width=1, fill_opacity=0.4, fill_color=c).shift(DOWN*0.5 + i*0.15*RIGHT)
            for i, c in enumerate([RED, GREEN, PURPLE])
        ]).next_to(conv_text, DOWN)
        
        arrow1 = Arrow(input_box.get_right(), conv_boxes.get_left(), buff=0.1)
        self.play(Create(arrow1))
        self.play(FadeIn(conv_text), FadeIn(conv_boxes))
        self.wait(0.3)
        
        # Max Pooling
        pool_text = Text("Max\nPool", font_size=18).shift(RIGHT*0.5 + UP)
        pool_boxes = VGroup(*[
            Rectangle(height=0.7, width=0.7, fill_opacity=0.5, fill_color=c).shift(DOWN*0.5 + i*0.12*RIGHT)
            for i, c in enumerate([RED, GREEN, PURPLE])
        ]).next_to(pool_text, DOWN)
        
        arrow2 = Arrow(conv_boxes.get_right(), pool_boxes.get_left(), buff=0.1)
        self.play(Create(arrow2))
        self.play(FadeIn(pool_text), FadeIn(pool_boxes))
        self.wait(0.3)
        
        # Flatten
        flat_text = Text("Flatten", font_size=18).shift(RIGHT*2.8 + UP)
        flat_nodes = VGroup(*[
            Circle(0.06, fill_opacity=1, fill_color=BLUE).shift(RIGHT*3.2 + UP*(0.8-i*0.16))
            for i in range(12)
        ])
        
        arrow3 = Arrow(pool_boxes.get_right(), flat_nodes.get_left(), buff=0.1)
        self.play(Create(arrow3))
        self.play(FadeIn(flat_text), FadeIn(flat_nodes))
        self.wait(0.3)
        
        # Fully Connected
        fc_text = Text("FC", font_size=18).shift(RIGHT*4.8 + UP*0.8)
        fc_nodes = VGroup(*[
            Circle(0.09, fill_opacity=1, fill_color=ORANGE).shift(RIGHT*5 + UP*(0.5-i*0.25))
            for i in range(6)
        ])
        
        # Connections
        lines = VGroup(*[
            Line(flat_nodes[j].get_center(), fc_nodes[i].get_center(), 
                 stroke_width=0.3, stroke_opacity=0.2)
            for i in range(6) for j in range(0, 12, 3)
        ])
        
        arrow4 = Arrow(flat_nodes.get_right(), fc_nodes.get_left(), buff=0.2)
        self.play(Create(arrow4), Create(lines))
        self.play(FadeIn(fc_text), FadeIn(fc_nodes))
        self.wait(0.3)
        
        # Output
        out_text = Text("Output", font_size=18).shift(RIGHT*6.2 + UP*0.3)
        outputs = VGroup(*[
            VGroup(
                Circle(0.11, fill_opacity=1, fill_color=GREEN).shift(RIGHT*6.3 + DOWN*(0.5+i*0.5)),
                Text(name, font_size=14).shift(RIGHT*6.8 + DOWN*(0.5+i*0.5))
            )
            for i, name in enumerate(["Cat", "Dog", "Bird"])
        ])
        
        out_lines = VGroup(*[
            Line(fc_nodes[j].get_center(), outputs[i][0].get_center(),
                 stroke_width=0.4, stroke_opacity=0.3)
            for i in range(3) for j in range(6)
        ])
        
        arrow5 = Arrow(fc_nodes.get_right(), outputs.get_left(), buff=0.2)
        self.play(Create(arrow5), Create(out_lines))
        self.play(FadeIn(out_text), FadeIn(outputs))
        self.wait(0.5)
        
        # Highlight winner
        self.play(
            outputs[0][0].animate.scale(1.3).set_color(GOLD),
            outputs[0][1].animate.set_color(GOLD).scale(1.2)
        )
        self.wait(1)
        
        # Summary
        summary = Text("Feature Extraction → Classification", font_size=28, color=YELLOW)
        summary.to_edge(DOWN)
        self.play(Write(summary))
        self.wait(2)
