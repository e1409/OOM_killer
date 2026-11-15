from manim import *
try:
    from .oom_memory import *
except ImportError:
    from oom_memory import *


class Scene06Recovery(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        heading = title('Восстановление')
        panel, blocks, swap, usage = memory_panel(RECOVERY)
        cards = process_cards(alive=False)
        self.add(heading,panel,cards)
        free = [i for i,c in enumerate(RECOVERY) if c==LIGHT]
        label = status('Свободно: 3,5 ГиБ',GREEN)
        self.play(*[blocks[i].animate.set_fill('#C7EFDA',opacity=1).set_stroke(GREEN,width=1.5) for i in free],FadeIn(label),run_time=1.3)
        self.wait(.7)
        self.play(*[blocks[i].animate.set_fill(LIGHT,opacity=1).set_stroke('#CAD3DF',width=1) for i in free],run_time=.8)
        for card, indices, color in [(cards[0], list(range(0,8)), BLUE), (cards[1], list(range(12,20)), PURPLE)]:
            arrow = Arrow(card.get_right(), blocks[indices[0]].get_left(), buff=.12, color=color, stroke_width=3)
            self.play(GrowArrow(arrow), Indicate(card, color=color), run_time=.6)
            self.play(*[Indicate(blocks[k], color=color) for k in indices], FadeOut(arrow), run_time=.9)
        self.play(Transform(label,status('Система работает',GREEN)),run_time=.8)
        self.wait(2)
        self.play(FadeOut(VGroup(heading,panel,cards,label)),run_time=.9)
