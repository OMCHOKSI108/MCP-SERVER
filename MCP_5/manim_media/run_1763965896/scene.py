from manim import *
import numpy as np

class CNNExplainer(Scene):
    def construct(self):
        # Title
        title = Text("Convolutional Neural Network", font_size=48, weight=BOLD)
        subtitle = Text("Image Classification Pipeline", font_size=28)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait()
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # Step 1: Input Image
        self.show_input_image()
        self.wait()
        
        # Step 2: Convolution Operation
        self.show_convolution()
        self.wait()
        
        # Step 3: Feature Maps
        self.show_feature_maps()
        self.wait()
        
        # Step 4: Max Pooling
        self.show_max_pooling()
        self.wait()
        
        # Step 5: Flatten
        self.show_flatten()
        self.wait()
        
        # Step 6: Fully Connected Layer
        self.show_fully_connected()
        self.wait()
        
        # Step 7: Output Classes
        self.show_output()
        self.wait(2)
    
    def show_input_image(self):
        # Create input image representation
        input_label = Text("Input Image (28×28)", font_size=32)
        input_label.to_edge(UP)
        
        # Create a grid representing an image
        grid = VGroup()
        for i in range(5):
            for j in range(5):
                shade = np.random.random()
                square = Square(side_length=0.3, fill_opacity=shade, 
                               fill_color=BLUE, stroke_width=1)
                square.move_to([j*0.3 - 0.6, -i*0.3 + 0.6, 0])
                grid.add(square)
        
        grid.scale(1.2)
        
        self.play(Write(input_label))
        self.play(Create(grid))
        self.wait()
        
        self.input_label = input_label
        self.input_grid = grid
    
    def show_convolution(self):
        # Show convolution operation
        conv_title = Text("Convolution with 3×3 Filters", font_size=28)
        conv_title.next_to(self.input_label, DOWN)
        
        # Create a 3x3 filter
        filter_grid = VGroup()
        filter_values = [[1, 0, -1], [1, 0, -1], [1, 0, -1]]
        
        for i in range(3):
            for j in range(3):
                square = Square(side_length=0.25, fill_opacity=0.7,
                               fill_color=YELLOW, stroke_width=2, stroke_color=ORANGE)
                square.move_to([j*0.25, -i*0.25, 0])
                
                val_text = Text(str(filter_values[i][j]), font_size=16)
                val_text.move_to(square.get_center())
                
                filter_grid.add(VGroup(square, val_text))
        
        filter_grid.scale(1.5)
        filter_grid.next_to(self.input_grid, RIGHT, buff=1)
        
        filter_label = Text("Filter", font_size=20)
        filter_label.next_to(filter_grid, DOWN)
        
        arrow = Arrow(self.input_grid.get_right(), filter_grid.get_left(), 
                     buff=0.3, color=WHITE)
        
        self.play(Write(conv_title))
        self.play(Create(filter_grid), Write(filter_label))
        self.play(GrowArrow(arrow))
        self.wait()
        
        self.play(FadeOut(self.input_label), FadeOut(self.input_grid),
                 FadeOut(conv_title), FadeOut(filter_grid), 
                 FadeOut(filter_label), FadeOut(arrow))
    
    def show_feature_maps(self):
        # Show multiple feature maps
        feature_title = Text("Feature Maps", font_size=32)
        feature_title.to_edge(UP)
        
        feature_maps = VGroup()
        colors = [RED, GREEN, BLUE, PURPLE]
        
        for idx, color in enumerate(colors):
            fmap = VGroup()
            for i in range(4):
                for j in range(4):
                    intensity = np.random.random() * 0.8 + 0.2
                    square = Square(side_length=0.2, fill_opacity=intensity,
                                   fill_color=color, stroke_width=1)
                    square.move_to([j*0.2, -i*0.2, 0])
                    fmap.add(square)
            
            fmap.move_to([idx*1.8 - 2.7, -0.5, 0])
            feature_maps.add(fmap)
        
        self.play(Write(feature_title))
        self.play(LaggedStart(*[Create(fmap) for fmap in feature_maps], lag_ratio=0.2))
        self.wait()
        
        self.feature_title = feature_title
        self.feature_maps = feature_maps
    
    def show_max_pooling(self):
        # Show max pooling operation
        pool_title = Text("Max Pooling (2×2)", font_size=28)
        pool_title.next_to(self.feature_title, DOWN)
        
        # Show one feature map before and after pooling
        before = self.feature_maps[0].copy()
        before.scale(0.8).shift(LEFT * 3)
        
        after = VGroup()
        for i in range(2):
            for j in range(2):
                intensity = np.random.random() * 0.8 + 0.4
                square = Square(side_length=0.3, fill_opacity=intensity,
                               fill_color=RED, stroke_width=2)
                square.move_to([j*0.3 + 1, -i*0.3, 0])
                after.add(square)
        
        arrow = Arrow(before.get_right(), after.get_left(), buff=0.3)
        
        self.play(FadeOut(self.feature_maps), Write(pool_title))
        self.play(Create(before))
        self.play(GrowArrow(arrow), Create(after))
        self.wait()
        
        self.play(FadeOut(pool_title), FadeOut(before), 
                 FadeOut(arrow), FadeOut(self.feature_title))
        
        self.pooled = after
    
    def show_flatten(self):
        # Show flattening operation
        flatten_title = Text("Flatten", font_size=32)
        flatten_title.to_edge(UP)
        
        # Create vector representation
        vector = VGroup()
        for i in range(16):
            rect = Rectangle(width=0.3, height=0.15, 
                           fill_opacity=0.6, fill_color=TEAL,
                           stroke_width=1)
            rect.move_to([0, -i*0.18 + 1.4, 0])
            vector.add(rect)
        
        vector.next_to(self.pooled, RIGHT, buff=1.5)
        
        arrow = Arrow(self.pooled.get_right(), vector.get_left(), buff=0.3)
        
        self.play(Write(flatten_title))
        self.play(GrowArrow(arrow))
        self.play(Transform(self.pooled.copy(), vector))
        self.play(Create(vector))
        self.wait()
        
        self.play(FadeOut(flatten_title), FadeOut(self.pooled), FadeOut(arrow))
        
        self.vector = vector
    
    def show_fully_connected(self):
        # Show fully connected layer
        fc_title = Text("Fully Connected Layer", font_size=32)
        fc_title.to_edge(UP)
        
        # Create neurons
        fc_neurons = VGroup()
        for i in range(8):
            neuron = Circle(radius=0.15, fill_opacity=0.8, 
                          fill_color=ORANGE, stroke_width=2)
            neuron.move_to([2.5, -i*0.4 + 1.4, 0])
            fc_neurons.add(neuron)
        
        # Create connections
        connections = VGroup()
        for v_rect in self.vector[:8]:
            for neuron in fc_neurons:
                line = Line(v_rect.get_right(), neuron.get_left(),
                          stroke_width=0.5, stroke_opacity=0.3, color=GRAY)
                connections.add(line)
        
        self.play(Write(fc_title))
        self.play(Create(connections))
        self.play(Create(fc_neurons))
        self.wait()
        
        self.play(FadeOut(fc_title), FadeOut(self.vector), FadeOut(connections))
        
        self.fc_neurons = fc_neurons
    
    def show_output(self):
        # Show output classification
        output_title = Text("Output Classes", font_size=32, color=GOLD)
        output_title.to_edge(UP)
        
        # Create output neurons with labels
        classes = ["Cat", "Dog", "Bird"]
        output_layer = VGroup()
        
        for i, label in enumerate(classes):
            neuron = Circle(radius=0.25, fill_opacity=0.9,
                          fill_color=GREEN, stroke_width=3, stroke_color=GOLD)
            neuron.move_to([5, -i*1.2, 0])
            
            text = Text(label, font_size=24)
            text.next_to(neuron, RIGHT)
            
            # Probability
            prob = np.random.random()
            if i == 1:  # Highlight "Dog" as prediction
                prob = 0.85
                neuron.set_fill(color=GOLD)
            
            prob_text = Text(f"{prob:.2f}", font_size=20, color=YELLOW)
            prob_text.next_to(neuron, LEFT)
            
            output_layer.add(VGroup(neuron, text, prob_text))
        
        # Connections from FC to output
        connections = VGroup()
        for fc_neuron in self.fc_neurons:
            for out_group in output_layer:
                out_neuron = out_group[0]
                line = Line(fc_neuron.get_right(), out_neuron.get_left(),
                          stroke_width=0.5, stroke_opacity=0.2, color=YELLOW)
                connections.add(line)
        
        self.play(Write(output_title))
        self.play(Create(connections))
        self.play(LaggedStart(*[Create(group) for group in output_layer], lag_ratio=0.2))
        self.wait()
        
        # Highlight prediction
        prediction = Text("Prediction: Dog", font_size=36, color=GOLD, weight=BOLD)
        prediction.to_edge(DOWN)
        
        self.play(Write(prediction))
        self.play(output_layer[1][0].animate.scale(1.3))
        self.wait()
