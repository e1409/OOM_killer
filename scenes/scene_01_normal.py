
from manim import *
try:
    from .oom_memory import *
except ImportError:
    from oom_memory import *


class Scene01Normal(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        heading = title('Нормальная работа')
        cards = process_cards()
        panel, blocks, swap, usage = memory_panel(NORMAL)
        heap = heap_view(4, intro=True)

        self.play(FadeIn(heading), FadeIn(panel), run_time=1.3)
        self.play(
            LaggedStart(
                *[FadeIn(c, shift=RIGHT*.2) for c in cards],
                lag_ratio=.2
            ),
            run_time=1.5
        )
        self.play(FadeIn(heap), run_time=.8)
        self.wait(.8)

        for i in range(4):
            link = Arrow(
                heap[1][i].get_right(),
                blocks[8+i].get_left(),
                buff=.06,
                color=BLACK,
                stroke_width=2.5
            )
            self.play(
                GrowArrow(link),
                Indicate(heap[1][i], color=TEAL),
                run_time=.65
            )
            self.play(
                Indicate(blocks[8+i], color=TEAL),
                FadeOut(link),
                run_time=.65
            )

        # График потребления памяти
        x_axis = Arrow(
            [-5.35, -3.02, 0],
            [-1.15, -3.02, 0],
            buff=0,
            color='#CAD3DF',
            stroke_width=2.5,
            tip_length=.12
        )

        y_axis = Arrow(
            [-5.35, -3.02, 0],
            [-5.35, -2.12, 0],
            buff=0,
            color='#CAD3DF',
            stroke_width=2.5,
            tip_length=.12
        )

        rss_label = txt('RSS, ГиБ', -5.85, -2.08, 15, MUTED)
        t_label = txt('t', -1.03, -3.02, 15, MUTED)

        ticks = VGroup()
        numbers = VGroup()
        grid = VGroup()

        for value, y in [(1, -2.78), (2, -2.54), (3, -2.30)]:
            tick = Line(
                [-5.43, y, 0],
                [-5.27, y, 0],
                color='#CAD3DF',
                stroke_width=2
            )

            number = txt(value, -5.62, y, 14, MUTED)

            line = DashedLine(
                [-5.35, y, 0],
                [-1.30, y, 0],
                dash_length=.08,
                color='#D9E1EA',
                stroke_width=1.3
            )

            ticks.add(tick)
            numbers.add(number)
            grid.add(line)

        flat = Line(
            [-5.18, -2.78, 0],
            [-4.45, -2.78, 0],
            color=TEAL,
            stroke_width=4
        )

        stable = status('Стабильно', GREEN)

        self.play(
            Create(x_axis),
            Create(y_axis),
            FadeIn(rss_label),
            FadeIn(t_label),
            FadeIn(ticks),
            FadeIn(numbers),
            Create(grid),
            run_time=.8
        )

        self.play(Create(flat), run_time=.6)
        self.play(FadeIn(stable), run_time=.5)
        self.wait(2)

