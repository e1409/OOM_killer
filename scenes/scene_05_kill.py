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
        signal_text = status('SIGKILL (9)',RED)
        self.add(heading,panel,table,outline)
        self.play(FadeIn(signal_text), run_time=.8)
        self.play(Indicate(rows[1],color=RED),run_time=.8)
        self.wait(.4)
        kill_mark = Cross(rows[1], stroke_color=RED, stroke_width=3)
        self.play(Create(kill_mark), Transform(signal_text, status('Процесс завершается', RED)), run_time=.8)
        self.wait(.4)
        heap = heap_view(13,reserved=3,swapped=4)
        cards = process_cards(3.25)
        self.play(FadeOut(table),FadeOut(outline),FadeOut(kill_mark),FadeIn(cards),FadeIn(heap),run_time=.9)
        strike = Cross(cards[1],stroke_color=RED,stroke_width=3)
        self.play(Create(strike),run_time=.6)
        self.play(FadeOut(strike),FadeOut(cards[1]),Transform(signal_text,status('Освобождение памяти',GREEN)),run_time=.7)
        for j,group in enumerate([WORKER[:4],WORKER[4:8],WORKER[8:]]):
            offset = j*4
            self.play(*ram_change(blocks,group,LIGHT),
                      *[heap[1][4+offset+k].animate.set_opacity(0) for k in range(len(group))],
                      Transform(usage,usage_text(7.75-(offset+len(group))/4)),run_time=.85)
        self.play(*[c.animate.set_fill(LIGHT,opacity=1) for c in swap[1]],
                  *[heap[1][i].animate.set_opacity(0) for i in range(4)],
                  Transform(swap[0],txt('Swap  0/1 ГиБ',2.05,-2.72,18)),run_time=1.1)
        self.play(FadeOut(heap),Transform(signal_text,status('−3,25 ГиБ RAM   −1 ГиБ Swap',GREEN)),run_time=.8)
        self.wait(1.8)
