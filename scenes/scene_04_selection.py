
from manim import *
try:
    from .oom_memory import *
except ImportError:
    from oom_memory import *


class Scene04Selection(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        panel, blocks, swap, usage = memory_panel(PRESSURE, True)
        table, rows = score_table(final=False)

        heading = title('Выбор жертвы OOM')

        formula = txt(
            'Оценка ≈ 1000 × (RSS + swap) / T + adj',
            -3.10, -1.78, 18, DARK, True
        )

        terms = txt(
            'RSS = RAM процесса   T = 9 ГиБ',
            -3.10, -2.08, 15, MUTED
        )

        self.add(panel, heading, table, formula, terms)

        # Пояснение перед началом расчётов
        note_box = RoundedRectangle(
            width=4.8,
            height=.48,
            corner_radius=.08,
            stroke_color=ORANGE,
            stroke_width=1.8,
            fill_color='#FFF1DD',
            fill_opacity=1
        ).move_to([-3.10, -2.95, 0])

        note_text = txt(
            'Значение adj задаётся пользователем',
            -3.10, -2.95, 14, ORANGE, True
        )

        self.play(
            FadeIn(note_box),
            FadeIn(note_text),
            run_time=.5
        )

        self.wait(1.5)

        self.play(
            FadeOut(note_box),
            FadeOut(note_text),
            run_time=.4
        )

        # Расчёты в одну строку
        browser_calc = txt(
            'Оценка ≈ 1000 × (2 + 0) / 9 + 0 ≈ 222',
            -3.10, -3.18, 17, BLUE, True
        )

        worker_calc = txt(
            'Оценка ≈ 1000 × (3,25 + 1) / 9 + 200 ≈ 672',
            -3.10, -3.18, 17, TEAL, True
        )

        db_calc = txt(
            'Оценка ≈ 1000 × (2 + 0) / 9 − 100 ≈ 122',
            -3.10, -3.18, 17, PURPLE, True
        )

        # Все три расчёта одинакового масштаба
        scale = min(1, 5.4 / max(
            browser_calc.width,
            worker_calc.width,
            db_calc.width
        ))

        for calculation in [browser_calc, worker_calc, db_calc]:
            calculation.scale(scale)

        # Браузер
        calc_name = txt(
            'Браузер',
            -3.10, -2.84, 18, BLUE, True
        )

        calc_line = browser_calc

        self.play(
            FadeIn(calc_name),
            FadeIn(calc_line),
            Indicate(rows[0][1], color=BLUE),
            *[Indicate(blocks[i], color=BLUE) for i in range(8)],
            run_time=1.1
        )

        self.wait(1.2)

        # worker.py
        self.play(
            Transform(
                calc_name,
                txt('worker.py', -3.10, -2.84, 18, TEAL, True)
            ),
            Transform(calc_line, worker_calc),
            *[Indicate(blocks[i], color=TEAL) for i in WORKER],
            Indicate(swap[1], color=TEAL),
            run_time=1.2
        )

        self.play(
            Transform(
                rows[1][1],
                txt('672', -2.62, -.08, 24, DARK, True)
            ),
            run_time=1.0
        )

        self.wait(1.2)

        # База данных
        self.play(
            Transform(
                calc_name,
                txt('База данных', -3.10, -2.84, 18, PURPLE, True)
            ),
            Transform(calc_line, db_calc),
            *[
                Indicate(blocks[i], color=PURPLE)
                for i in range(12, 20)
            ],
            run_time=1.1
        )

        self.play(
            Transform(
                rows[2][1],
                txt('122', -2.62, -.86, 24, DARK, True)
            ),
            run_time=.9
        )

        self.wait(1.2)

        # Выбор процесса с максимальной оценкой
        outline = SurroundingRectangle(
            rows[1],
            color=RED,
            buff=.13,
            corner_radius=.09,
            stroke_width=3
        )

        self.play(
            Create(outline),
            rows[1][1].animate.set_color(RED),
            FadeOut(calc_name),
            FadeOut(calc_line),
            run_time=1.0
        )

        self.play(
            FadeIn(status('Максимум → worker.py', RED)),
            run_time=.6
        )

        self.wait(2)

