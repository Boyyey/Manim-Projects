from manim import *
import random

class LLMExplanation(Scene):
    def construct(self):
        # SCENE 1: The Magic Question
        cursor = Rectangle(height=0.5, width=0.1, fill_color=WHITE, fill_opacity=1)
        self.play(Blink(cursor))
        
        question = Text("How does an AI know what to say next?", font_size=36)
        self.play(Write(question), run_time=2)
        self.wait(1)
        
        # SCENE 2: Human Text → Tokens → Numbers
        sentence = Text("The astronaut walked on the...", font_size=32)
        self.play(ReplacementTransform(question, sentence))
        self.wait(0.5)
        
        # Animate tokenization
        tokens = ["The", "astronaut", "walked", "on", "the", "[...]"]
        token_boxes = VGroup(*[
            Rectangle(width=len(word)*0.3+0.4, height=0.8, fill_color=BLUE_E, fill_opacity=0.7)
            .add(Text(word, font_size=24).set_z_index(1))
            for word in tokens
        ]).arrange(RIGHT, buff=0.2)
        
        self.play(Transform(sentence, token_boxes))
        self.wait(1)
        
        # Convert to numbers
        numbers = VGroup(*[
            Text(str(random.randint(1000,9999)), font_size=24)
            .move_to(box.get_center())
            for box in token_boxes
        ])
        self.play(Transform(token_boxes, numbers))
        self.wait(1)
        
        # SCENE 3: Neural Network Reveal
        nn = self.create_neural_network()
        self.play(
            FadeOut(token_boxes),
            Create(nn),
            run_time=2
        )
        
        # Animate data flowing through
        particles = self.flow_particles_through_network(nn)
        self.play(particles, run_time=3)
        
        # SCENE 4: Attention Mechanism
        # Safely get attention node (middle layer, middle node)
        attention_node = nn[1][min(3, len(nn[1])-1)]  # Using min to prevent index errors
        self.play(
            attention_node.animate.set_fill(RED, opacity=0.8),
            Flash(attention_node, color=RED, flash_radius=1.5)
        )
        
        # Create attention lines to valid nodes only
        attention_lines = VGroup()
        valid_indices = [i for i in [0, 3, 5] if i < len(nn[0])]  # Filter valid indices
        for i in valid_indices:
            line = Line(
                nn[0][i].get_center(),
                attention_node.get_center(),
                stroke_width=3,
                color=YELLOW
            )
            attention_lines.add(line)
        
        self.play(Create(attention_lines), run_time=1.5)
        self.wait(1)
        
        # SCENE 5: Word Prediction
        options = ["moon", "floor", "stars", "kitchen"]
        word_cloud = VGroup(*[
            Text(word, font_size=28).shift(random.uniform(-1,1)*RIGHT + random.uniform(-1,1)*UP)
            for word in options
        ]).arrange_in_grid(rows=2, cols=2, buff=1)
        
        self.play(FadeIn(word_cloud))
        self.wait(0.5)
        
        # Highlight correct prediction
        moon = word_cloud[0]
        self.play(
            moon.animate.scale(1.5).set_color(GREEN),
            *[FadeOut(word, scale=0.5) for word in word_cloud[1:]]
        )
        self.wait(1)
        
        # SCENE 6: Scaling the Mind
        final_text = VGroup(
            Text("Language Models don't understand like humans...", font_size=32),
            Text("but they're trained on how we do.", font_size=32),
            Text("Billions of voices, now speaking through one.", font_size=24, color=GOLD)
        )
        final_text.arrange(DOWN, buff=0.5).center()
        
        self.play(
            FadeOut(nn),
            FadeOut(attention_lines),
            FadeOut(moon),
            Write(final_text),
            run_time=3
        )
        self.wait(3)
    
    def create_neural_network(self):
        """Creates a visually impressive neural network with safe layer sizes"""
        layers = [6, 8, 6, 4]  # More balanced layer sizes
        colors = [BLUE_B, TEAL, GREEN_B, YELLOW]
        
        network = VGroup()
        for i, nodes in enumerate(layers):
            layer = VGroup()
            for j in range(nodes):
                node = Circle(radius=0.3)
                node.set_fill(colors[i], opacity=0.3)
                node.set_stroke(colors[i], width=2)
                layer.add(node)
            layer.arrange(DOWN, buff=0.4)
            layer.shift(i * 2.5 * RIGHT - (len(layers)-1)*1.25 * RIGHT)
            network.add(layer)
        
        # Add connections with fading opacity
        for i in range(len(layers)-1):
            for node1 in network[i]:
                for node2 in network[i+1]:
                    line = Line(
                        node1.get_center(),
                        node2.get_center(),
                        stroke_width=1.5,
                        stroke_opacity=0.3
                    )
                    network.add(line)
        
        return network
    
    def flow_particles_through_network(self, nn):
        """Creates particle flow animation through the network"""
        particles = VGroup()
        paths = []
        
        # Create paths through the network
        for _ in range(20):
            path = VMobject()
            points = []
            for layer in nn[:-1]:  # Skip output layer
                if len(layer) > 0:  # Only if layer has nodes
                    node = random.choice(layer)
                    points.append(node.get_center())
            if points:  # Only add path if we have points
                path.set_points_smoothly(points)
                paths.append(path)
        
        # Create particles for each path
        for path in paths:
            particle = Dot(radius=0.08, color=random.choice([BLUE, GREEN, YELLOW]))
            particle.move_to(path.get_start())
            particles.add(particle)
            
            # Animate along path
            particle.generate_target()
            particle.target.move_to(path.get_end())
        
        return AnimationGroup(*[
            MoveAlongPath(particle, path, rate_func=linear)
            for particle, path in zip(particles, paths)
        ], lag_ratio=0.1)

class Blink(Animation):
    def __init__(self, cursor, **kwargs):
        super().__init__(cursor, **kwargs)
        self.cursor = cursor
        
    def interpolate_mobject(self, alpha):
        if alpha < 0.5:
            self.cursor.set_opacity(1)
        else:
            self.cursor.set_opacity(0)