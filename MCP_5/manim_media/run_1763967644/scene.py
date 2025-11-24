from manim import *
import numpy as np

class CNNExplainer(Scene):
    def construct(self):
        # Title
        title = Text("Convolutional Neural Network", font_size=42, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.5)
        
        # Step 1: Input Image
        input_label = Text("Input Image", font_size=24).shift(UP*2 + LEFT*5)
        input_image = Square(side_length=1.3, fill_opacity=0.3, fill_color=BLUE)
        input_image.next_to(input_label, DOWN, buff=0.3)
        
        # Add grid to represent pixels
        grid = VGroup()
        for i in range(6):
            for j in range(6):
                pixel = Square(side_length=0.2, stroke_width=1)
                pixel.move_to(input_image.get_center() + 
                            RIGHT*(i-2.5)*0.21 + UP*(2.5-j)*0.21)
                pixel.set_fill(color=interpolate_color(BLUE, WHITE, np.random.random()), opacity=0.5)
                grid.add(pixel)
        
        self.play(FadeIn(input_label), Create(input_image))
        self.play(FadeIn(grid))
        self.wait(0.5)
        
        # Step 2: Convolution
        conv_label = Text("Convolution\n3×3 Filters", font_size=20).shift(UP*2 + LEFT*2.5)
        
        filter_box = Square(side_length=0.5, color=YELLOW, stroke_width=3)
        filter_box.next_to(conv_label, DOWN, buff=0.2)
        filter_text = Text("3×3", font_size=14).move_to(filter_box.get_center())
        
        feature_maps = VGroup()
        for i in range(3):
            fmap = Rectangle(height=1, width=1, fill_opacity=0.4)
            fmap.set_fill(color=[RED, GREEN, PURPLE][i])
            fmap.next_to(conv_label, DOWN, buff=0.2 + i*0.25)
            fmap.shift(RIGHT*0.7)
            feature_maps.add(fmap)
        
        self.play(FadeIn(conv_label), Create(filter_box), Write(filter_text))
        arrow1 = Arrow(input_image.get_right(), filter_box.get_left(), buff=0.1, color=YELLOW)
        self.play(Create(arrow1))
        arrow2 = Arrow(filter_box.get_right(), feature_maps.get_left(), buff=0.1, color=YELLOW)
        self.play(Create(arrow2), LaggedStart(*[FadeIn(fmap) for fmap in feature_maps], lag_ratio=0.2))
        self.wait(0.5)
        
        # Step 3: Max Pooling
        pool_label = Text("Max Pooling", font_size=20).shift(UP*2 + RIGHT*1)
        
        pooled_maps = VGroup()
        for i in range(3):
            pmap = Rectangle(height=0.7, width=0.7, fill_opacity=0.5)
            pmap.set_fill(color=[RED, GREEN, PURPLE][i])
            pmap.next_to(pool_label, DOWN, buff=0.2 + i*0.2)
            pmap.shift(RIGHT*0.5)
            pooled_maps.add(pmap)
        
        self.play(FadeIn(pool_label))
        arrow3 = Arrow(feature_maps.get_right(), pooled_maps.get_left(), buff=0.1, color=ORANGE)
        self.play(Create(arrow3), 
                 LaggedStart(*[TransformFromCopy(feature_maps[i], pooled_maps[i]) 
                             for i in range(3)], lag_ratio=0.2))
        self.wait(0.5)
        
        # Step 4: Flatten
        flatten_label = Text("Flatten", font_size=20).shift(UP*2 + RIGHT*3.5)
        
        flattened = VGroup()
        for i in range(10):
            node = Circle(radius=0.07, fill_opacity=0.8, color=BLUE_C)
            node.shift(RIGHT*4 + UP*(1 - i*0.2))
            flattened.add(node)
        
        self.play(FadeIn(flatten_label))
        arrow4 = Arrow(pooled_maps.get_right(), flattened.get_left(), buff=0.1, color=TEAL)
        self.play(Create(arrow4), 
                 LaggedStart(*[FadeIn(node) for node in flattened], lag_ratio=0.05))
        self.wait(0.5)
        
        # Step 5: Fully Connected
        fc_label = Text("Fully\nConnected", font_size=18).shift(UP*2 + RIGHT*5.2)
        
        fc_layer = VGroup()
        for i in range(5):
            node = Circle(radius=0.1, fill_opacity=0.8, color=ORANGE)
            node.shift(RIGHT*5.5 + UP*(0.6 - i*0.3))
            fc_layer.add(node)
        
        connections = VGroup()
        for flat_node in flattened[::2]:
            for fc_node in fc_layer:
                line = Line(flat_node.get_center(), fc_node.get_center(), 
                          stroke_width=0.4, stroke_opacity=0.2, color=GRAY)
                connections.add(line)
        
        self.play(FadeIn(fc_label))
        self.play(Create(connections))
        self.play(LaggedStart(*[FadeIn(node) for node in fc_layer], lag_ratio=0.1))
        self.wait(0.5)
        
        # Step 6: Output Classes
        output_label = Text("Output", font_size=18).shift(UP*1.5 + RIGHT*6.5)
        
        outputs = VGroup()
        classes = ["Cat", "Dog", "Bird"]
        for i, name in enumerate(classes):
            node = Circle(radius=0.12, fill_opacity=0.9, color=GREEN)
            node.shift(DOWN*1 + RIGHT*6 + UP*(0.5 - i*0.5))
            label = Text(name, font_size=14).next_to(node, RIGHT, buff=0.15)
            outputs.add(VGroup(node, label))
        
        output_connections = VGroup()
        for fc_node in fc_layer:
            for output_group in outputs:
                line = Line(fc_node.get_center(), output_group[0].get_center(),
                          stroke_width=0.6, stroke_opacity=0.3, color=GOLD)
                output_connections.add(line)
        
        self.play(FadeIn(output_label))
        self.play(Create(output_connections))
        self.play(LaggedStart(*[FadeIn(out) for out in outputs], lag_ratio=0.2))
        self.wait(0.5)
        
        # Highlight winner
        self.play(
            outputs[0][0].animate.set_fill(color=GOLD, opacity=1).scale(1.2),
            outputs[0][1].animate.set_color(GOLD).scale(1.1)
        )
        self.wait(1)
        
        # Summary
        summary = Text("CNN: Feature Extraction → Classification", font_size=28, color=YELLOW)
        summary.to_edge(DOWN, buff=0.4)
        self.play(Write(summary))
        self.wait(2)