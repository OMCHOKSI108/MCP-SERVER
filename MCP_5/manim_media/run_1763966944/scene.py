from manim import *

class TestScene(Scene):
    def construct(self):
        text = Text("Hello")
        self.play(Write(text))
        self.wait(1)
