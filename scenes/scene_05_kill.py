
from manim import *
try:
    from .oom_memory import *
except ImportError:
    from oom_memory import *


class Scene05Kill(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        heading = title('Завершение процесса')
        panel, blocks, swap, usage = memory_panel(PRESSURE,True)
        table, rows = score_table(final=True, selected=True)
        outline = SurroundingRectangle(rows[1],color=RED,buff=.13,corner_radius=.09,stroke_width=3)
        self.add(heading,panel,table,outline)

        sender_box = RoundedRectangle(
            width=3.25,
            height=.72,
            corner_radius=.10,
            stroke_color=RED,
            stroke_width=2,
            fill_color='#FCE8E6',
            fill_opacity=1
        ).move_to([-3.95,-2.15,0])

        sender_text = txt(
            'oom_kill_process()',
            -3.95, -2.15, 19, RED, True
        )

        # Ломаная стрелка:
        # вправо, вверх, затем влево к worker.py
        start = sender_box.get_right()
        elbow_x = 0.55
        target_y = rows[1].get_center()[1]
        end = outline.get_right() + RIGHT * 0.02

        arrow_horizontal = Line(
            start,
            [elbow_x, start[1], 0],
            color=RED,
            stroke_width=3
        )

        arrow_vertical = Line(
            [elbow_x, start[1], 0],
            [elbow_x, target_y, 0],
            color=RED,
            stroke_width=3
        )

        # Более длинная стрелка с заметным наконечником
        kill_arrow = Arrow(
            [elbow_x, target_y, 0],
            [end[0], target_y, 0],
            buff=0,
            color=RED,
            stroke_width=3,
            tip_length=.22,
            max_tip_length_to_length_ratio=.35
        )

        arrow_label = txt(
            'SIGKILL (9)',
            -1.28, -1.85, 19, RED, True
        )

        sender_group = VGroup(
            sender_box,
            sender_text,
            arrow_horizontal,
            arrow_vertical,
            kill_arrow,
            arrow_label
        )

        self.play(
            FadeIn(sender_box),
            FadeIn(sender_text),
            Create(arrow_horizontal),
            Create(arrow_vertical),
            GrowArrow(kill_arrow),
            FadeIn(arrow_label),
            run_time=.8
        )

        self.play(
            Indicate(rows[1],color=RED),
            run_time=.8
        )
        self.wait(.4)

        signal_text = status('Процесс завершается', RED)
        kill_mark = Cross(
            rows[1],
            stroke_color=RED,
            stroke_width=3
        )

        self.play(
            FadeOut(sender_group),
            Create(kill_mark),
            FadeIn(signal_text),
            run_time=.8
        )

        self.wait(.4)

        heap = heap_view(13,reserved=3,swapped=4)
        cards = process_cards(3.25)

        self.play(
            FadeOut(table),
            FadeOut(outline),
            FadeOut(kill_mark),
            FadeIn(cards),
            FadeIn(heap),
            run_time=.9
        )

        # Зачёркиваем worker.py
        strike = Cross(
            cards[1],
            stroke_color=RED,
            stroke_width=3
        )

        self.play(
            Create(strike),
            run_time=.6
        )

        # Не убираем зачёркнутую карточку worker.py
        self.play(
            Transform(
                signal_text,
                status('Освобождение памяти',GREEN)
            ),
            run_time=.7
        )

        # Освобождение RAM
        for j,group in enumerate([
            WORKER[:4],
            WORKER[4:8],
            WORKER[8:]
        ]):
            offset = j*4

            self.play(
                *ram_change(blocks,group,LIGHT),
                *[
                    heap[1][4+offset+k].animate.set_opacity(0)
                    for k in range(len(group))
                ],
                Transform(
                    usage,
                    usage_text(
                        7.75-(offset+len(group))/4
                    )
                ),
                run_time=.85
            )

        # Освобождение swap
        self.play(
            *[
                c.animate.set_fill(LIGHT,opacity=1)
                for c in swap[1]
            ],
            *[
                heap[1][i].animate.set_opacity(0)
                for i in range(4)
            ],
            Transform(
                swap[0],
                txt(
                    'Swap  0/1 ГиБ',
                    2.05,-2.72,18
                )
            ),
            run_time=1.1
        )

        self.play(
            FadeOut(heap),
            Transform(
                signal_text,
                status(
                    '−3,25 ГиБ RAM   −1 ГиБ Swap',
                    GREEN
                )
            ),
            run_time=.8
        )

        self.wait(1.8)
