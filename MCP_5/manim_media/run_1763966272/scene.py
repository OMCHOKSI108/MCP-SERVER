from manim import *
import numpy as np

class CNNExplainer(Scene):
    def construct(self):
        # Title
        title = Text("Convolutional Neural Network", font_size=48)
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeOut(title))
        
        # Step 1: Input Image
        input_label = Text("Input Image", font_size=32).to_edge(UP)
        grid = self.create_image_grid()
        grid.shift(LEFT * 4)
        
        self.play(Write(input_label), Create(grid))
        self.wait()
        
        # Step 2: Convolution
        conv_label = Text("3×3 Convolution", font_size=28)
        conv_label.next_to(grid, DOWN)
        filter_box = self.create_filter()
        filter_box.next_to(grid, RIGHT, buff=1)
        
        arrow1 = Arrow(grid.get_right(), filter_box.get_left(), buff=0.2)
        
        self.play(Write(conv_label), Create(filter_box), GrowArrow(arrow1))
        self.wait()
        
        # Step 3: Feature Maps
        feature_maps = self.create_feature_maps()
        feature_maps.next_to(filter_box, RIGHT, buff=1)
        arrow2 = Arrow(filter_box.get_right(), feature_maps.get_left(), buff=0.2)
        
        self.play(GrowArrow(arrow2), Create(feature_maps))
        self.wait()
        
        # Clear and show pooling
        self.play(
            FadeOut(input_label), FadeOut(grid), FadeOut(conv_label),
            FadeOut(filter_box), FadeOut(arrow1)
        )
        
        # Step 4: Max Pooling
        pool_label = Text("Max Pooling (2×2)", font_size=32).to_edge(UP)
        feature_maps.generate_target()
        feature_maps.target.shift(LEFT * 3)
        
        pooled = self.create_pooled_map()
        pooled.next_to(feature_maps.target, RIGHT, buff=1.5)
        arrow3 = Arrow(feature_maps.target.get_right(), pooled.get_left(), buff=0.2)
        
        self.play(Write(pool_label), MoveToTarget(feature_maps), FadeOut(arrow2))
        self.play(GrowArrow(arrow3), Create(pooled))
        self.wait()
        
        # Step 5: Flatten
        self.play(FadeOut(pool_label), FadeOut(feature_maps), FadeOut(arrow3))
        
        flatten_label = Text("Flatten", font_size=32).to_edge(UP)
        pooled.generate_target()
        pooled.target.shift(LEFT * 2)
        
        vector = self.create_vector()
        vector.next_to(pooled.target, RIGHT, buff=1.5)
        arrow4 = Arrow(pooled.target.get_right(), vector.get_left(), buff=0.2)
        
        self.play(Write(flatten_label), MoveToTarget(pooled))
        self.play(GrowArrow(arrow4), Create(vector))
        self.wait()
        
        # Step 6: Fully Connected
        self.play(FadeOut(flatten_label), FadeOut(pooled), FadeOut(arrow4))
        
        fc_label = Text("Fully Connected", font_size=32).to_edge(UP)
        vector.generate_target()
        vector.target.shift(LEFT * 1)
        
        fc_neurons = self.create_fc_layer()
        fc_neurons.next_to(vector.target, RIGHT, buff=1.5)
        
        self.play(Write(fc_label), MoveToTarget(vector))
        self.play(Create(fc_neurons))
        self.wait()
        
        # Step 7: Output
        self.play(FadeOut(fc_label), FadeOut(vector))
        
        output_label = Text("Output Classes", font_size=32, color=GOLD).to_edge(UP)
        fc_neurons.generate_target()
        fc_neurons.target.shift(LEFT * 1.5)
        
        output = self.create_output_layer()
        output.next_to(fc_neurons.target, RIGHT, buff=1.5)
        
        self.play(Write(output_label), MoveToTarget(fc_neurons))
        self.play(Create(output))
        
        prediction = Text("Prediction: Dog", font_size=36, color=GOLD).to_edge(DOWN)
        self.play(Write(prediction))
        self.wait(2)
    
    def create_image_grid(self):
        grid = VGroup()
        for i in range(4):
            for j in range(4):
                shade = 0.3 + 0.5 * np.random.random()
                square = Square(side_length=0.25, fill_opacity=shade,
                               fill_color=BLUE, stroke_width=1)
                square.move_to([j*0.25, -i*0.25, 0])
                grid.add(square)
        return grid
    
    def create_filter(self):
        filter_grid = VGroup()
        for i in range(3):
            for j in range(3):
                square = Square(side_length=0.2, fill_opacity=0.7,
                               fill_color=YELLOW, stroke_width=2)
                square.move_to([j*0.2, -i*0.2, 0])
                filter_grid.add(square)
        return filter_grid
    
    def create_feature_maps(self):
        maps = VGroup()
        for k in range(3):
            fmap = VGroup()
            for i in range(3):
                for j in range(3):
                    intensity = 0.4 + 0.5 * np.random.random()
                    square = Square(side_length=0.15, fill_opacity=intensity,
                                   fill_color=RED, stroke_width=0.5)
                    square.move_to([j*0.15, -i*0.15, 0])
                    fmap.add(square)
            fmap.shift(DOWN * k * 0.7)
            maps.add(fmap)
        return maps
    
    def create_pooled_map(self):
        pooled = VGroup()
        for i in range(2):
            for j in range(2):
                intensity = 0.5 + 0.4 * np.random.random()
                square = Square(side_length=0.3, fill_opacity=intensity,
                               fill_color=ORANGE, stroke_width=2)
                square.move_to([j*0.3, -i*0.3, 0])
                pooled.add(square)
        return pooled
    
    def create_vector(self):
        vector = VGroup()
        for i in range(12):
            rect = Rectangle(width=0.25, height=0.12, fill_opacity=0.7,
                           fill_color=TEAL, stroke_width=1)
            rect.move_to([0, -i*0.14 + 0.8, 0])
            vector.add(rect)
        return vector
    
    def create_fc_layer(self):
        neurons = VGroup()
        for i in range(6):
            neuron = Circle(radius=0.12, fill_opacity=0.8,
                          fill_color=PURPLE, stroke_width=2)
            neuron.move_to([0, -i*0.35 + 0.7, 0])
            neurons.add(neuron)
        return neurons
    
    def create_output_layer(self):
        output = VGroup()
        classes = ["Cat", "Dog", "Bird"]
        colors = [RED, GOLD, GREEN]
        
        for i, (cls, color) in enumerate(zip(classes, colors)):
            neuron = Circle(radius=0.2, fill_opacity=0.9,
                          fill_color=color, stroke_width=2)
            neuron.move_to([0, -i*0.8, 0])
            
            label = Text(cls, font_size=20)
            label.next_to(neuron, RIGHT, buff=0.2)
            
            output.add(VGroup(neuron, label))
        
        return output
