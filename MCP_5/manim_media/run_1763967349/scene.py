from manim import *
import numpy as np

class CNNExplainer(Scene):
    def construct(self):
        # Title
        title = Text("Convolutional Neural Network (CNN)", font_size=48, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        # Step 1: Input Image
        input_label = Text("Input Image", font_size=28).shift(UP*2.5 + LEFT*5)
        input_image = Square(side_length=1.5, fill_opacity=0.3, fill_color=BLUE)
        input_image.next_to(input_label, DOWN, buff=0.3)
        
        # Add grid pattern to represent pixels
        grid = VGroup()
        for i in range(8):
            for j in range(8):
                pixel = Square(side_length=0.18, stroke_width=1)
                pixel.move_to(input_image.get_center() + 
                            RIGHT*(i-3.5)*0.19 + UP*(3.5-j)*0.19)
                pixel.set_fill(color=interpolate_color(BLUE, WHITE, np.random.random()), opacity=0.6)
                grid.add(pixel)
        
        self.play(FadeIn(input_label), Create(input_image))
        self.play(FadeIn(grid))
        self.wait(0.5)
        
        # Step 2: Convolution with 3x3 filter
        conv_label = Text("Convolution\n3×3 Filters", font_size=24).shift(UP*2.5 + LEFT*2)
        
        # Show filter
        filter_box = Square(side_length=0.6, color=YELLOW, stroke_width=3)
        filter_box.next_to(conv_label, DOWN, buff=0.3)
        filter_text = Text("3×3\nFilter", font_size=16).move_to(filter_box.get_center())
        
        # Feature maps
        feature_maps = VGroup()
        for i in range(3):
            fmap = Rectangle(height=1.2, width=1.2, fill_opacity=0.4)
            fmap.set_fill(color=[RED, GREEN, PURPLE][i])
            fmap.next_to(conv_label, DOWN, buff=0.3 + i*0.3)
            fmap.shift(RIGHT*0.8)
            feature_maps.add(fmap)
        
        self.play(FadeIn(conv_label), Create(filter_box), Write(filter_text))
        self.wait(0.3)
        
        # Animate convolution
        arrow1 = Arrow(input_image.get_right(), filter_box.get_left(), buff=0.1, color=YELLOW)
        self.play(Create(arrow1))
        self.wait(0.3)
        
        arrow2 = Arrow(filter_box.get_right(), feature_maps.get_left(), buff=0.1, color=YELLOW)
        self.play(Create(arrow2), LaggedStart(*[FadeIn(fmap) for fmap in feature_maps], lag_ratio=0.2))
        self.wait(0.5)
        
        # Step 3: Max Pooling
        pool_label = Text("Max Pooling\n2×2", font_size=24).shift(UP*2.5 + RIGHT*1.5)
        
        pooled_maps = VGroup()
        for i in range(3):
            pmap = Rectangle(height=0.8, width=0.8, fill_opacity=0.5)
            pmap.set_fill(color=[RED, GREEN, PURPLE][i])
            pmap.next_to(pool_label, DOWN, buff=0.3 + i*0.25)
            pmap.shift(RIGHT*0.6)
            pooled_maps.add(pmap)
        
        self.play(FadeIn(pool_label))
        arrow3 = Arrow(feature_maps.get_right(), pooled_maps.get_left(), buff=0.1, color=ORANGE)
        self.play(Create(arrow3), 
                 LaggedStart(*[TransformFromCopy(feature_maps[i], pooled_maps[i]) 
                             for i in range(3)], lag_ratio=0.2))
        self.wait(0.5)
        
        # Step 4: Flatten
        flatten_label = Text("Flatten", font_size=24).shift(UP*2.5 + RIGHT*4)
        
        flattened = VGroup()
        for i in range(12):
            node = Circle(radius=0.08, fill_opacity=0.8, color=BLUE_C)
            node.shift(RIGHT*4.8 + UP*(1.2 - i*0.22))
            flattened.add(node)
        
        self.play(FadeIn(flatten_label))
        arrow4 = Arrow(pooled_maps.get_right(), flattened.get_left(), buff=0.1, color=TEAL)
        self.play(Create(arrow4), 
                 LaggedStart(*[FadeIn(node) for node in flattened], lag_ratio=0.05))
        self.wait(0.5)
        
        # Step 5: Fully Connected Layer
        fc_label = Text("Fully\nConnected", font_size=22).shift(UP*2.5 + RIGHT*5.8)
        
        fc_layer = VGroup()
        for i in range(6):
            node = Circle(radius=0.12, fill_opacity=0.8, color=ORANGE)
            node.shift(RIGHT*6.2 + UP*(0.8 - i*0.32))
            fc_layer.add(node)
        
        # Connections from flattened to FC
        connections = VGroup()
        for flat_node in flattened[:6]:
            for fc_node in fc_layer:
                line = Line(flat_node.get_center(), fc_node.get_center(), 
                          stroke_width=0.5, stroke_opacity=0.3, color=GRAY)
                connections.add(line)
        
        self.play(FadeIn(fc_label))
        arrow5 = Arrow(flattened.get_right(), fc_layer.get_left(), buff=0.2, color=PINK)
        self.play(Create(connections), Create(arrow5))
        self.play(LaggedStart(*[FadeIn(node) for node in fc_layer], lag_ratio=0.1))
        self.wait(0.5)
        
        # Step 6: Output Classes
        output_label = Text("Output\nClasses", font_size=22).shift(UP*2 + RIGHT*6.8)
        output_label.scale(0.8)
        
        outputs = VGroup()
        class_names = ["Cat", "Dog", "Bird"]
        for i, name in enumerate(class_names):
            node = Circle(radius=0.15, fill_opacity=0.9, color=GREEN)
            node.shift(DOWN*1.5 + RIGHT*6.2 + UP*(0.6 - i*0.6))
            
            label = Text(name, font_size=16).next_to(node, RIGHT, buff=0.2)
            
            # Probability bar
            prob = 0.8 if i == 0 else 0.1 + i*0.05
            prob_bar = Rectangle(height=0.15, width=prob*0.8, 
                                fill_opacity=0.7, fill_color=YELLOW,
                                stroke_width=1)
            prob_bar.next_to(node, RIGHT, buff=0.05)
            
            outputs.add(VGroup(node, label, prob_bar))
        
        # Connections from FC to output
        output_connections = VGroup()
        for fc_node in fc_layer:
            for output_group in outputs:
                line = Line(fc_node.get_center(), output_group[0].get_center(),
                          stroke_width=0.8, stroke_opacity=0.4, color=GOLD)
                output_connections.add(line)
        
        self.play(FadeIn(output_label))
        self.play(Create(output_connections))
        self.play(LaggedStart(*[FadeIn(out) for out in outputs], lag_ratio=0.2))
        self.wait(1)
        
        # Final emphasis - highlight the winning class
        winner = outputs[0][0]
        winner_label = outputs[0][1]
        self.play(
            winner.animate.set_fill(color=GOLD, opacity=1).scale(1.3),
            winner_label.animate.set_color(GOLD).scale(1.2),
            run_time=0.8
        )
        self.wait(1)
        
        # Summary text
        summary = Text("CNN: Extract features → Classify", font_size=32, color=YELLOW)
        summary.to_edge(DOWN, buff=0.5)
        self.play(Write(summary))
        self.wait(2)
        
        self.play(FadeOut(VGroup(*self.mobjects)))
        self.wait(0.5)