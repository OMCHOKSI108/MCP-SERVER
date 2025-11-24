from manim import *

class CNNExplainer(Scene):
    def construct(self):
        # Title
        title = Text("CNN Architecture", font_size=40)
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeOut(title))
        
        # Create all layers
        input_img = Square(1.5, fill_opacity=0.5, fill_color=BLUE)
        input_img.shift(LEFT * 5)
        input_text = Text("Input\n28×28", font_size=18).next_to(input_img, DOWN, buff=0.2)
        
        conv = Rectangle(height=1.8, width=0.3, fill_opacity=0.7, fill_color=YELLOW)
        conv.next_to(input_img, RIGHT, buff=0.8)
        conv_text = Text("Conv\n3×3", font_size=18).next_to(conv, DOWN, buff=0.2)
        
        feature = VGroup(*[
            Rectangle(height=1.2, width=0.15, fill_opacity=0.6, fill_color=RED).shift(RIGHT * i * 0.2)
            for i in range(3)
        ])
        feature.next_to(conv, RIGHT, buff=0.8)
        feature_text = Text("Feature\nMaps", font_size=18).next_to(feature, DOWN, buff=0.2)
        
        pool = Rectangle(height=1.0, width=0.2, fill_opacity=0.6, fill_color=ORANGE)
        pool.next_to(feature, RIGHT, buff=0.8)
        pool_text = Text("Max\nPool", font_size=18).next_to(pool, DOWN, buff=0.2)
        
        flatten = Rectangle(height=2.0, width=0.15, fill_opacity=0.5, fill_color=TEAL)
        flatten.next_to(pool, RIGHT, buff=0.8)
        flatten_text = Text("Flatten", font_size=18).next_to(flatten, DOWN, buff=0.2)
        
        fc = VGroup(*[
            Circle(radius=0.15, fill_opacity=0.7, fill_color=PURPLE).shift(DOWN * i * 0.4)
            for i in range(5)
        ])
        fc.next_to(flatten, RIGHT, buff=0.8)
        fc_text = Text("Fully\nConnected", font_size=18).next_to(fc, DOWN, buff=0.3)
        
        output = VGroup(*[
            Circle(radius=0.2, fill_opacity=0.8, fill_color=GREEN).shift(DOWN * i * 0.6)
            for i in range(3)
        ])
        output.next_to(fc, RIGHT, buff=0.8)
        output_text = Text("Output\nClasses", font_size=18).next_to(output, DOWN, buff=0.2)
        
        # Class labels
        labels = VGroup(
            Text("Cat", font_size=16).next_to(output[0], RIGHT, buff=0.2),
            Text("Dog", font_size=16).next_to(output[1], RIGHT, buff=0.2),
            Text("Bird", font_size=16).next_to(output[2], RIGHT, buff=0.2)
        )
        
        # Create arrows
        arrows = VGroup(*[
            Arrow(input_img.get_right(), conv.get_left(), buff=0.1),
            Arrow(conv.get_right(), feature.get_left(), buff=0.1),
            Arrow(feature.get_right(), pool.get_left(), buff=0.1),
            Arrow(pool.get_right(), flatten.get_left(), buff=0.1),
            Arrow(flatten.get_right(), fc.get_left(), buff=0.1),
            Arrow(fc.get_right(), output.get_left(), buff=0.1)
        ])
        
        # Animate
        self.play(Create(input_img), Write(input_text))
        self.wait(0.3)
        
        self.play(GrowArrow(arrows[0]))
        self.play(Create(conv), Write(conv_text))
        self.wait(0.3)
        
        self.play(GrowArrow(arrows[1]))
        self.play(Create(feature), Write(feature_text))
        self.wait(0.3)
        
        self.play(GrowArrow(arrows[2]))
        self.play(Create(pool), Write(pool_text))
        self.wait(0.3)
        
        self.play(GrowArrow(arrows[3]))
        self.play(Create(flatten), Write(flatten_text))
        self.wait(0.3)
        
        self.play(GrowArrow(arrows[4]))
        self.play(Create(fc), Write(fc_text))
        self.wait(0.3)
        
        self.play(GrowArrow(arrows[5]))
        self.play(Create(output), Write(output_text))
        self.play(Write(labels))
        self.wait(0.5)
        
        # Highlight prediction
        prediction = Text("Prediction: Dog (85%)", font_size=28, color=GOLD)
        prediction.to_edge(DOWN)
        self.play(Write(prediction))
        self.play(output[1].animate.set_fill(GOLD, opacity=1).scale(1.2))
        self.wait(2)
