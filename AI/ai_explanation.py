from manim import *

class AIExplanation(Scene):
    def construct(self):
        # Title
        title = Text("Understanding Artificial Intelligence", font_size=48)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))
        
        # Part 1: What is AI?
        what_is_ai = Text("What is Artificial Intelligence?", font_size=36)
        self.play(Write(what_is_ai))
        self.wait(1.5)
        self.play(what_is_ai.animate.to_edge(UP))
        
        # Human brain vs computer
        brain = SVGMobject("brain").scale(0.8)
        chip = SVGMobject("computer_chip").scale(0.8)
        
        brain_label = Text("Human Brain", font_size=24).next_to(brain, DOWN)
        chip_label = Text("AI System", font_size=24).next_to(chip, DOWN)
        
        brain_group = VGroup(brain, brain_label)
        chip_group = VGroup(chip, chip_label)
        
        brain_group.shift(LEFT*3)
        chip_group.shift(RIGHT*3)
        
        arrow = Arrow(brain.get_right(), chip.get_left(), buff=0.2)
        arrow_label = Text("Inspired by", font_size=20).next_to(arrow, UP)
        
        self.play(FadeIn(brain_group), FadeIn(chip_group))
        self.play(GrowArrow(arrow), Write(arrow_label))
        self.wait(2)
        
        # Definition
        definition = Text(
            "AI systems are designed to perform tasks\n"
            "that typically require human intelligence",
            font_size=28,
            t2c={"human intelligence": YELLOW}
        )
        definition.next_to(what_is_ai, DOWN, buff=1)
        
        self.play(Write(definition))
        self.wait(3)
        self.play(FadeOut(brain_group), FadeOut(chip_group), 
                 FadeOut(arrow), FadeOut(arrow_label),
                 definition.animate.move_to(ORIGIN))
        
        # Part 2: How AI Learns
        how_title = Text("How Does AI Learn?", font_size=36).to_edge(UP)
        self.play(ReplacementTransform(what_is_ai, how_title))
        self.play(FadeOut(definition))
        
        # Data -> Model -> Prediction flow
        data_icon = SVGMobject("database").scale(0.7)
        model_icon = SVGMobject("neural_network").scale(0.7)
        prediction_icon = SVGMobject("light_bulb").scale(0.7)
        
        data_label = Text("Data", font_size=24).next_to(data_icon, DOWN)
        model_label = Text("Model", font_size=24).next_to(model_icon, DOWN)
        prediction_label = Text("Prediction", font_size=24).next_to(prediction_icon, DOWN)
        
        data_group = VGroup(data_icon, data_label)
        model_group = VGroup(model_icon, model_label)
        prediction_group = VGroup(prediction_icon, prediction_label)
        
        data_group.shift(LEFT*4)
        prediction_group.shift(RIGHT*4)
        
        arrow1 = Arrow(data_icon.get_right(), model_icon.get_left(), buff=0.2)
        arrow2 = Arrow(model_icon.get_right(), prediction_icon.get_left(), buff=0.2)
        
        self.play(FadeIn(data_group))
        self.play(GrowArrow(arrow1), FadeIn(model_group))
        self.play(GrowArrow(arrow2), FadeIn(prediction_group))
        self.wait(2)
        
        # Training explanation
        training_text = Text(
            "AI learns patterns from data\n"
            "through a process called training",
            font_size=28
        ).next_to(how_title, DOWN, buff=1)
        
        self.play(Write(training_text))
        self.wait(3)
        
        # Part 3: Neural Network Example
        nn_title = Text("Neural Networks: A Common AI Approach", font_size=36).to_edge(UP)
        self.play(
            ReplacementTransform(how_title, nn_title),
            FadeOut(training_text),
            FadeOut(data_group), FadeOut(model_group), FadeOut(prediction_group),
            FadeOut(arrow1), FadeOut(arrow2)
        )
        
        # Simple neural network diagram
        input_layer = VGroup(*[Circle(radius=0.3, color=BLUE) for _ in range(3)])
        input_layer.arrange(DOWN, buff=0.5)
        input_layer.shift(LEFT*3)
        
        hidden_layer = VGroup(*[Circle(radius=0.3, color=GREEN) for _ in range(4)])
        hidden_layer.arrange(DOWN, buff=0.4)
        
        output_layer = VGroup(*[Circle(radius=0.3, color=RED) for _ in range(2)])
        output_layer.arrange(DOWN, buff=0.8)
        output_layer.shift(RIGHT*3)
        
        # Connections
        connections = VGroup()
        for input_node in input_layer:
            for hidden_node in hidden_layer:
                connections.add(Line(input_node, hidden_node, stroke_width=1.5))
        for hidden_node in hidden_layer:
            for output_node in output_layer:
                connections.add(Line(hidden_node, output_node, stroke_width=1.5))
        
        # Labels
        input_label = Text("Input", font_size=24).next_to(input_layer, DOWN)
        hidden_label = Text("Hidden Layers", font_size=24).next_to(hidden_layer, DOWN)
        output_label = Text("Output", font_size=24).next_to(output_layer, DOWN)
        
        self.play(
            LaggedStart(
                *[FadeIn(node) for node in input_layer],
                *[FadeIn(node) for node in hidden_layer],
                *[FadeIn(node) for node in output_layer],
                lag_ratio=0.1
            )
        )
        self.play(Create(connections), run_time=2)
        self.play(Write(input_label), Write(hidden_label), Write(output_label))
        self.wait(2)
        
        # Activation animation
        pulse_group = VGroup()
        for node in input_layer:
            pulse_group.add(node.copy().set(color=YELLOW, fill_opacity=0))
        
        self.play(LaggedStart(
            *[Succession(
                node.animate.set_fill(BLUE, opacity=0.8),
                node.animate.set_fill(BLUE, opacity=0)
            ) for node in input_layer],
            lag_ratio=0.2
        ))
        
        # Show data flowing through
        for i, input_node in enumerate(input_layer):
            for j, hidden_node in enumerate(hidden_layer):
                line = connections[i*len(hidden_layer)+j]
                dot = Dot(color=YELLOW).move_to(input_node.get_center())
                self.play(
                    dot.animate.move_to(hidden_node.get_center()),
                    rate_func=linear,
                    run_time=0.5
                )
                self.remove(dot)
        
        # Conclusion
        conclusion = Text(
            "AI is transforming our world by\n"
            "learning from data and making predictions",
            font_size=32,
            t2c={"transforming": YELLOW, "learning": GREEN, "predictions": RED}
        )
        
        self.play(
            FadeOut(input_layer), FadeOut(hidden_layer), FadeOut(output_layer),
            FadeOut(connections), FadeOut(input_label), FadeOut(hidden_label), FadeOut(output_label),
            FadeOut(nn_title)
        )
        self.play(Write(conclusion))
        self.wait(3)
        self.play(FadeOut(conclusion))
        
        # Final message
        final = Text("The Future of AI is Exciting!", font_size=42, color=YELLOW)
        self.play(Write(final))
        self.wait(2)
        self.play(FadeOut(final))