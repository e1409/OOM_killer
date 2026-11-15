from manim import *
try:
    from .oom_memory import *
except ImportError:
    from oom_memory import *


class Scene03Pressure(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        cards = process_cards(3)
        panel, blocks, swap, usage = memory_panel(GROWTH)
        heap = heap_view(12)
        heading = title('Нехватка памяти')
        caption = status('Запрос +2 ГиБ',ORANGE)
        self.add(heading,cards,panel,heap,caption)
        self.play(*[heap[1][i].animate.set_stroke(TEAL,width=2.5) for i in range(12,20)],run_time=1)
        self.wait(.6)
        self.play(Transform(caption,status('Page fault',ORANGE)),Indicate(heap[1][12],color=ORANGE),run_time=.8)
        fault = txt('Нужна страница в RAM',0,-3.72,16,MUTED)
        self.play(FadeIn(fault),run_time=.3)
        self.wait(1.8)
        self.play(FadeOut(fault),run_time=.3)

        # Чистая файловая страница уже сохранена в файле; её не надо писать в swap.
        file_icon = VGroup(cell('#FFF1DD',.72,.84),txt('Файл',0,0,15,ORANGE)).move_to([.1,.65,0])
        line = DashedLine(file_icon.get_right(),blocks[22].get_left(),color=CACHE,stroke_width=2)
        self.play(FadeIn(file_icon),Create(line),Indicate(blocks[22],color=ORANGE),
                  Transform(caption,status('Освобождение файлового кэша',ORANGE)),run_time=.9)
        old_cache = blocks[22].copy()
        self.add(old_cache)
        self.play(FadeOut(old_cache,shift=UP*.35),blocks[22].animate.set_fill(LIGHT,opacity=1),
                  Transform(usage,usage_text(7.5)),run_time=1.2)
        self.play(FadeOut(line),FadeOut(file_icon),run_time=.5)
        self.wait(.5)

        # В swap сохраняем содержимое четырёх холодных анонимных групп.
        disk = VGroup(cell('#EDF2F7',1.25,.65),
                      txt('Диск',0,0,18,MUTED,True)).move_to([.05,-2.65,0])
        swap_link = Arrow(disk.get_right(),swap[0].get_left(),buff=.08,color=MUTED,stroke_width=2)
        self.play(FadeIn(disk),GrowArrow(swap_link),
                  Transform(caption,status('Swap',ORANGE)),run_time=.8)
        self.play(Indicate(swap[1],color=TEAL),run_time=.8)
        self.wait(1.0)
        self.play(FadeOut(disk),FadeOut(swap_link),
                  Transform(caption,status('RAM → Swap',ORANGE)),
                  *[Indicate(blocks[i],color=TEAL) for i in range(8,12)],run_time=.8)
        moving = VGroup(*[blocks[i].copy() for i in range(8,12)])
        self.add(moving)
        self.play(*[Transform(moving[j],swap[1][j].copy().set_fill(TEAL,opacity=1)) for j in range(4)],
                  *ram_change(blocks,range(8,12),LIGHT),
                  *[heap[1][i].animate.set_fill(SWAP,opacity=1) for i in range(4)],
                  Transform(usage,usage_text(6.5)),rss_change(cards,2),run_time=1.8)
        for c in swap[1]:
            c.set_fill(TEAL,opacity=1)
        self.remove(moving)
        self.play(Transform(swap[0],txt('Swap  1/1 ГиБ',2.05,-2.72,18)),run_time=.4)
        self.wait(.5)

        self.play(Transform(caption,status('Повторное выделение',TEAL)),run_time=.6)
        for j,i in enumerate([8,9,10,11,22]):
            page = heap[1][12+j]
            self.play(Indicate(page,color=TEAL),run_time=.22)
            token = page.copy().set_fill(TEAL,opacity=1)
            self.add(token)
            self.play(Transform(token,blocks[i].copy().set_fill(TEAL,opacity=1)),run_time=.45)
            blocks[i].set_fill(TEAL,opacity=1)
            page.set_fill(TEAL,opacity=1)
            self.remove(token)
            self.play(Transform(usage,usage_text(6.5+(j+1)/4)),rss_change(cards,2+(j+1)/4),run_time=.25)
        self.wait(.5)

        # Не весь запрос 2 ГиБ, а очередная физическая страница не выделяется.
        page = heap[1][17]
        self.play(Transform(caption,status('Page fault',ORANGE)),Indicate(page,color=ORANGE),run_time=.65)
        self.wait(1.3)
        token = page.copy().set_fill(TEAL,opacity=1)
        self.add(token)
        target = blocks[31]
        self.play(token.animate.move_to(target.get_center()+LEFT*.9),run_time=.8)
        cross = Cross(target,stroke_color=RED,stroke_width=4)
        self.play(Create(cross),target.animate.set_stroke(RED,width=2.5),
                  Transform(caption,status('Выделение не удалось',RED)),run_time=.6)
        self.play(token.animate.move_to(page),run_time=.5)
        self.remove(token)

        # Оценка возможности дальнейшего reclaim: символически, без выдуманного порога.
        check = VGroup(txt('Свободно + можно освободить',-3.25,-2.40,17,MUTED),
                       txt('< порога зоны',-3.25,-2.78,20,RED,True))
        self.play(FadeIn(check),Indicate(swap[1],color=ORANGE),run_time=.9)
        self.wait(1.5)
        warning = RoundedRectangle(width=5.1,height=.72,corner_radius=.12,
                                   stroke_color=RED,stroke_width=2.5,fill_color='#FCE8E6',fill_opacity=1)
        warning.move_to([0,-3.32,0])
        warning_text = txt('!  OUT OF MEMORY',0,-3.32,26,RED,True)
        self.play(FadeOut(check),FadeOut(cross),FadeOut(caption),
                  target.animate.set_stroke('#CAD3DF',width=1),
                  FadeIn(warning),FadeIn(warning_text),run_time=.9)
        self.play(Indicate(warning,color=RED,scale_factor=1.03),run_time=.7)
        self.wait(2)
