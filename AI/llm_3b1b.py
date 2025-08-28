from manim import *
import numpy as np

class LLM3B1B(Scene):
    def construct(self):
        # SCENE 1: Introduction
        title = Tex("How Large Language Models Work", font_size=48)
        subtitle = Tex("A Mathematical Perspective", font_size=36, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(Write(title), Write(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))

        # SCENE 2: Text to Numbers
        self.show_tokenization()

        # SCENE 3: Neural Network Architecture
        self.show_neural_network()

        # SCENE 4: Attention Mechanism
        self.show_attention()

        # SCENE 5: Training Process
        self.show_training()

        # Final Explanation
        self.show_conclusion()

    def show_tokenization(self):
     # Create sentence with proper spacing
     sentence = Tex("The astronaut walked on the...", font_size=36)
     self.play(Write(sentence))
     self.wait()

     # Tokenization animation
     tokens = ["The", "astronaut", "walked", "on", "the", "[...]"]
     token_boxes = VGroup(*[
        SurroundingRectangle(
            Tex(token, font_size=24),
            color=BLUE,
            buff=0.2,
            stroke_width=2
        ) for token in tokens
     ]).arrange(RIGHT, buff=0.3)
     token_boxes.next_to(sentence, DOWN, buff=1.0)

     self.play(
        Transform(sentence, sentence.copy().to_edge(UP)),
        LaggedStart(*[Create(box) for box in token_boxes], lag_ratio=0.2)
     )
     self.wait()

     # Show embedding space
     embedding_explanation = Tex(
        r"Each token $\rightarrow$ 512-4096 dimensional vector",
        font_size=30
     )
     embedding_explanation.next_to(token_boxes, DOWN, buff=1.0)
     self.play(Write(embedding_explanation))
     self.wait(2)

     # Fade out tokenization elements BEFORE neural network appears
     self.play(
        FadeOut(token_boxes),
        FadeOut(embedding_explanation),
        FadeOut(sentence),  # This is what was missing - fade out the sentence
        run_time=1
     )


    def show_neural_network(self):
     # Keep the sentence at the top (don't move it)
     # Create network layers with balanced spacing
     layers = VGroup()
     layer_sizes = [4, 8, 8, 4]  # Input, hidden, hidden, output
     colors = [BLUE, GREEN, GREEN, RED]
     layer_spacing = 3.0

     for i, size in enumerate(layer_sizes):
        layer = VGroup()
        for _ in range(size):
            neuron = Circle(radius=0.2, color=colors[i], fill_opacity=0.1)
            layer.add(neuron)
        layer.arrange(DOWN, buff=0.4)
        layer.shift(i * layer_spacing * RIGHT - (len(layer_sizes)-1)*layer_spacing/2 * RIGHT)
        layers.add(layer)
    
     # Position network lower to make room for the sentence at top
     layers.shift(DOWN*0.5)

     # Add connections
     connections = VGroup()
     for i in range(len(layer_sizes)-1):
        for neuron1 in layers[i]:
            for neuron2 in layers[i+1]:
                line = Line(
                    neuron1.get_center(),
                    neuron2.get_center(),
                    stroke_width=1,
                    stroke_opacity=0.3
                )
                connections.add(line)

     self.play(
        LaggedStart(*[Create(layer) for layer in layers], lag_ratio=0.2),
        run_time=2
     )
     self.play(
        Create(connections),
        run_time=3,
        lag_ratio=0.1
     )
     self.wait()

     dim_label = Tex(r"$\sim$100B parameters", font_size=30)
     dim_label.next_to(layers, DOWN, buff=0.8)
     self.play(Write(dim_label))
     self.wait(2)

     # Store these for later scenes
     self.network_layers = layers
     self.network_connections = connections
     self.parameters_label = dim_label

    def show_attention(self):
     # Label input and output nodes
     input_words = ["The", "astronaut", "walked", "on"]
     output_words = ["moon", "floor", "stars", "?"]

     input_labels = VGroup()
     for i, word in enumerate(input_words):
        label = Tex(word, font_size=20, color=BLUE)
        label.next_to(self.network_layers[0][i], LEFT, buff=0.3)
        input_labels.add(label)

     output_labels = VGroup()
     for i, word in enumerate(output_words):
        label = Tex(word, font_size=20, color=RED)
        label.next_to(self.network_layers[-1][i], RIGHT, buff=0.3)
        output_labels.add(label)

     self.play(
        LaggedStart(*[Write(label) for label in input_labels], lag_ratio=0.2),
        LaggedStart(*[Write(label) for label in output_labels], lag_ratio=0.2)
     )
     self.wait()

     # Highlight "astronaut" input (position 1)
     focus_word = input_labels[1]
     self.play(
        focus_word.animate.set_color(YELLOW),
        Flash(focus_word, color=YELLOW, flash_radius=0.5),
        run_time=1.5
     )

     # Create the complete path from "astronaut" to "moon"
     important_connections = VGroup()
    
     # Start from "astronaut" neuron (layer 0, position 1)
     start_neuron = self.network_layers[0][1]
    
     # We want to connect to "moon" (output layer position 0)
     # This requires finding connections through intermediate layers
     for i in range(len(self.network_layers)-1):
        next_layer = i+1
        # For the final connection, target position 0 ("moon")
        target_pos = 0 if next_layer == len(self.network_layers)-1 else 1
        
        for connection in self.network_connections:
            if (np.allclose(connection.get_start(), start_neuron.get_center()) and
                np.allclose(connection.get_end(), self.network_layers[next_layer][target_pos].get_center())):
                important_connections.add(connection)
                start_neuron = self.network_layers[next_layer][target_pos]
                break

     self.play(
        important_connections.animate.set_stroke(width=3, opacity=1, color=YELLOW),
        run_time=2
     )
     self.wait()

     # Highlight correct output "moon" (position 0)
     correct_output = output_labels[0]
     self.play(
        correct_output.animate.set_color(GREEN).scale(1.2),
        Flash(correct_output, color=GREEN, flash_radius=0.5),
        run_time=1.5
     )
     self.wait(2)

     # Clean up
     self.play(
        FadeOut(input_labels),
        FadeOut(output_labels),
        important_connections.animate.set_stroke(width=1, opacity=0.3, color=WHITE),
        run_time=1
     )
    
    def show_training(self):
     # Clear previous elements with proper fading
     self.play(
        FadeOut(self.network_layers),
        FadeOut(self.network_connections),
        FadeOut(self.parameters_label),
        run_time=1
     )
    
     # Set up clean space for training explanation
     training_title = Tex("Training Process", font_size=42)
     training_title.to_edge(UP)
     self.play(Write(training_title))
    
     # Equation with perfect spacing
     equation = MathTex(
        r"\theta_{t+1} = \theta_t - \alpha \nabla_\theta \mathcal{L}(\theta_t)",
        font_size=36
     )
     equation.shift(UP*0.5)  # Adjusted position
    
     # Explanation text with generous buffer
     explanation = Tex(
        "Adjusting weights to minimize prediction error",
        font_size=30
     )
     explanation.next_to(equation, DOWN, buff=0.8)  # Increased buffer
    
     # Visual example with ample spacing
     example_words = VGroup(
        Tex("The", font_size=24),
        Tex("astronaut", font_size=24),
        Tex("walked", font_size=24), 
        Tex("on", font_size=24)
     ).arrange(RIGHT, buff=0.5)
     example_words.next_to(explanation, DOWN, buff=1.0)
    
     # Animated gradient descent curve
     gd_curve = ParametricFunction(
        lambda t: np.array([t, -np.exp(-(t-1)**2), 0]),
        t_range=[0,2],
        color=BLUE
     )
     gd_curve.next_to(example_words, DOWN, buff=1.0)
    
     # Draw everything with perfect sequencing
     self.play(Write(equation))
     self.wait(0.5)
     self.play(Write(explanation))
     self.wait(0.5)
     self.play(FadeIn(example_words))
     self.wait(0.5)
     self.play(Create(gd_curve))
    
     # Animate optimization process
     dot = Dot(color=RED).move_to(gd_curve.get_start())
     self.play(MoveAlongPath(dot, gd_curve), run_time=3)
     self.wait()

     # Clean up training scene
     self.play(
        FadeOut(training_title),
        FadeOut(equation),
        FadeOut(explanation),
        FadeOut(example_words),
        FadeOut(gd_curve),
        FadeOut(dot))
        
    def show_conclusion(self):
        # Final explanation with perfect vertical spacing
        conclusion1 = Tex(
            "LLMs learn statistical patterns in language",
            font_size=36
        )
        conclusion2 = Tex(
            "through exposure to billions of examples",
            font_size=36
        ).next_to(conclusion1, DOWN, buff=0.6)
        conclusion3 = Tex(
            "without explicit understanding",
            font_size=36,
            color=RED
        ).next_to(conclusion2, DOWN, buff=0.6)

        self.play(Write(conclusion1))
        self.wait(0.5)
        self.play(Write(conclusion2))
        self.wait(0.5)
        self.play(Write(conclusion3))
        self.wait(3)

        # Final clean up
        self.play(FadeOut(conclusion1), FadeOut(conclusion2), FadeOut(conclusion3))