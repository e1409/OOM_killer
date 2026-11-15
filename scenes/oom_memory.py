from manim import *

BLUE = '#4B91E2'
TEAL = '#35B6A4'
PURPLE = '#9979D4'
LIGHT = '#EDF2F7'
SYSTEM = '#8995A3'
CACHE = '#E9B458'
SWAP = '#B8E6DF'
MUTED = '#66758A'
DARK = '#192B45'
GREEN = '#278B66'
ORANGE = '#C27B1A'
RED = '#C64747'

# Один блок — группа страниц суммарным объёмом 0,25 ГиБ.
NORMAL = [BLUE]*8 + [TEAL]*4 + [PURPLE]*8 + [SYSTEM]*2 + [CACHE] + [LIGHT]*9
GROWTH = NORMAL[:23] + [TEAL]*8 + [LIGHT]
PRESSURE = GROWTH.copy()
PRESSURE[22] = TEAL
RECOVERY = [LIGHT if c == TEAL else c for c in PRESSURE]
WORKER = [i for i, color in enumerate(PRESSURE) if color == TEAL]
SCORES = [('Браузер', 2, 0, 0), ('worker.py', 3.25, 1, 200), ('База данных', 2, 0, -100)]

Text.set_default(font='DejaVu Sans')


def txt(text, x, y, size=24, color=DARK, bold=False):
    return Text(str(text), font_size=size, color=color,
                weight=BOLD if bold else 'NORMAL').move_to([x, y, 0])


def gib(value):
    return f'{value:g}'.replace('.', ',')


def cell(color, w=0.78, h=0.32):
    return RoundedRectangle(width=w, height=h, corner_radius=0.04,
                            stroke_color='#CAD3DF', stroke_width=1,
                            fill_color=color, fill_opacity=1)


def ram_blocks(colors):
    return VGroup(*[cell(c).move_to([3.2+(i%4-1.5)*0.84,
                                    0.15+(i//4-3.5)*0.375, 0])
                    for i, c in enumerate(colors)])


def memory_legend():
    items = VGroup()
    for name, color in [('Система', SYSTEM), ('Кэш', CACHE), ('Свободно', LIGHT)]:
        items.add(VGroup(cell(color, .16, .16), Text(name, font_size=16, color=MUTED))
                  .arrange(RIGHT, buff=.07))
    return items.arrange(RIGHT, buff=.22).move_to([3.2,-2.10,0])


def swap_blocks(filled=False):
    blocks = VGroup(*[cell(TEAL if filled else LIGHT, .45, .32) for _ in range(4)])
    blocks.arrange(RIGHT, buff=.07).move_to([4.12,-2.72,0])
    return VGroup(txt('Swap  '+('1/1' if filled else '0/1')+' ГиБ', 2.05,-2.72,18), blocks)


def usage_text(used):
    return txt(f'{gib(used)} / 8 ГиБ', 3.2,-1.70,24,DARK,True)


def memory_panel(colors, filled=False):
    blocks = ram_blocks(colors)
    swap = swap_blocks(filled)
    usage = usage_text(sum(c != LIGHT for c in colors)/4)
    panel = VGroup(txt('RAM',3.2,2.20,30,DARK,True),
                   txt('блок = 0,25 ГиБ',3.2,1.87,16,MUTED),
                   blocks, usage, memory_legend(), swap)
    return panel, blocks, swap, usage


def process_cards(rss=1, alive=True):
    cards = VGroup()
    for i,(name, value, color) in enumerate([('Браузер',2,BLUE),('worker.py',rss,TEAL),('База данных',2,PURPLE)]):
        if not alive and i == 1:
            continue
        y = 1.53 - i*.78
        rect = RoundedRectangle(width=4.75,height=.61,corner_radius=.10,
                                stroke_color=color,stroke_width=2,
                                fill_color=color,fill_opacity=.10).move_to([-3.25,y,0])
        dot = Dot([-5.34,y,0],radius=.075,color=color)
        name_text = txt(name,-3.80,y,21)
        value_text = txt(gib(value)+' ГиБ',0,y,19,color,True)
        value_text.align_to(rect, RIGHT).shift(LEFT*.18)
        cards.add(VGroup(rect,dot,name_text,value_text))
    return cards


def heap_view(rss, reserved=0, swapped=0, intro=False):
    cells = VGroup()
    for i in range(20):
        color = SWAP if i < swapped else TEAL if i < swapped+rss else LIGHT
        frame = cell(color,.40,.30)
        if i < swapped+rss+reserved:
            frame.set_stroke(TEAL,width=1.6)
        frame.move_to([-3.25+(i%10-4.5)*.46,-1.12-(i//10)*.37,0])
        cells.add(frame)
    legend = VGroup()
    for name, color in [('RAM', TEAL), ('Swap', SWAP)]:
        legend.add(VGroup(cell(color,.17,.17), Text(name,font_size=15,color=MUTED)).arrange(RIGHT,buff=.07))
    legend.arrange(RIGHT,buff=.25).move_to([-3.25,-1.94,0])
    return VGroup(txt('Heap worker.py',-3.25,-.73,19,DARK,True),cells,legend)


def title(text):
    return txt(text,0,3.15,36,DARK,True)


def status(text, color=MUTED):
    return txt(text,0,-3.33,25,color,True)


def ram_change(blocks, indices, color):
    return [blocks[i].animate.set_fill(color,opacity=1) for i in indices]


def rss_change(cards, value):
    old = cards[1][3]
    new = txt(gib(value)+' ГиБ',0,.75,19,TEAL,True)
    new.align_to(cards[1][0], RIGHT).shift(LEFT*.18)
    return Transform(old,new)


def score_value(rss, swap, adj):
    return round(1000*(rss+swap)/9+adj)


def score_bar(value,color,y):
    bar = RoundedRectangle(width=3.8*value/800,height=.32,corner_radius=.04,
                           stroke_width=0,fill_color=color,fill_opacity=1)
    return bar.move_to([-5.55+bar.width/2,y,0])


def score_rows(final=True, selected=False):
    rows = VGroup()
    for i,(name,rss,swap,adj) in enumerate(SCORES):
        y = 1.15-i*1.12
        color = [BLUE,TEAL,PURPLE][i]
        value = score_value(rss,swap,adj if final else 0)
        name_text = txt(name,-4.27,y+.37,21,color,True)
        adj_text = txt(f'{adj:+d}' if adj else '0',-1.55,y+.37,19,MUTED)
        track = cell(LIGHT,3.8,.32).move_to([-3.65,y,0])
        bar = score_bar(value,color,y)
        number = txt(value,-1.27,y,23,RED if selected and i==1 else DARK,True)
        rows.add(VGroup(name_text,adj_text,track,bar,number))
    return rows


def score_table(final=False, selected=False):
    frame = RoundedRectangle(width=6.9, height=3.15, corner_radius=0.12,
                             stroke_color='#D7DEE8', stroke_width=2,
                             fill_color=WHITE, fill_opacity=0).move_to([-3.25, 0.38, 0])
    h1 = txt('Процесс', -4.85, 1.58, 17, MUTED)
    h2 = txt('Оценка', -2.65, 1.58, 17, MUTED)
    h3 = txt('adj', -1.00, 1.58, 17, MUTED)
    line = Line([-5.95, 1.25, 0], [-0.55, 1.25, 0], color='#D7DEE8')
    rows = VGroup()
    for i, (name, rss, swap, adj) in enumerate(SCORES):
        y = 0.70 - i * 0.78
        color = [BLUE, TEAL, PURPLE][i]
        value = score_value(rss, swap, adj if final else 0)
        name_text = txt(name, -4.70, y, 21, color, i==1)
        score_text = txt(value, -2.62, y, 24, RED if selected and i == 1 else DARK, True)
        adj_text = txt(f'{adj:+d}' if adj else '0', -1.00, y, 21, MUTED)
        rows.add(VGroup(name_text, score_text, adj_text))
    return VGroup(frame, h1, h2, h3, line, rows), rows
