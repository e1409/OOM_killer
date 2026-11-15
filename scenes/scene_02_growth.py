
from manim import *
try:
    from .oom_memory import *
except ImportError:
    from oom_memory import *


class Scene02Growth(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        heading = title('Рост памяти')
        cards = process_cards()
        panel, blocks, swap, usage = memory_panel(NORMAL)
        heap = heap_view(4)

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

        graph = VGroup(
            Line(
                [-5.18, -2.78, 0],
                [-4.45, -2.78, 0],
                color=TEAL,
                stroke_width=4
            )
        )

        self.add(
            heading, cards, panel, heap,
            grid, x_axis, y_axis,
            rss_label, t_label,
            ticks, numbers, graph
        )

        caption = status('Накопление данных', ORANGE)

        self.play(
            FadeIn(caption),
            Indicate(cards[1], color=TEAL),
            run_time=1.1
        )
        self.wait(.7)

        points = [
            (-3.75, -2.66),
            (-3.05, -2.54),
            (-2.35, -2.42),
            (-1.65, -2.30)
        ]

        values = [1.5, 2, 2.5, 3]

        for j in range(4):
            h = [4+2*j, 5+2*j]
            r = [23+2*j, 24+2*j]

            self.play(
                *[
                    heap[1][i].animate.set_stroke(TEAL, width=2.5)
                    for i in h
                ],
                run_time=.45
            )
            self.wait(.3)

            copies = VGroup(
                *[
                    heap[1][i].copy().set_fill(TEAL, opacity=1)
                    for i in h
                ]
            )
            self.add(copies)

            self.play(
                *[
                    copies[k].animate.move_to(blocks[r[k]])
                    .stretch_to_fit_width(.78)
                    .stretch_to_fit_height(.32)
                    for k in range(2)
                ],
                run_time=.7
            )

            blocks[r[0]].set_fill(TEAL, opacity=1)
            blocks[r[1]].set_fill(TEAL, opacity=1)

            for i in h:
                heap[1][i].set_fill(TEAL, opacity=1)

            self.remove(copies)

            segment = Line(
                graph[-1].get_end(),
                [points[j][0], points[j][1], 0],
                color=TEAL,
                stroke_width=4
            )

            self.play(
                Create(segment),
                rss_change(cards, values[j]),
                Transform(
                    usage,
                    usage_text(5.75+values[j]-1)
                ),
                run_time=.55
            )

            graph.add(segment)

        self.play(
            Indicate(blocks[31], color=ORANGE),
            Transform(
                caption,
                status('RAM почти заполнена', ORANGE)
            ),
            run_time=1
        )

        self.wait(1.6)

