---
### Официальная документация Linux Kernel 6.12
---

- [Назначение OOM-killer и условия его запуска](https://docs.kernel.org/6.12/admin-guide/mm/concepts.html#oom-killer)
- [Виртуальная память и выделение физических страниц](https://docs.kernel.org/6.12/admin-guide/mm/concepts.html#anonymous-memory)
- [Освобождение памяти](https://docs.kernel.org/6.12/admin-guide/mm/concepts.html#reclaim)
- [Принципы выбора страниц для освобождения](https://docs.kernel.org/6.12/mm/multigen_lru.html)
- [Использование Swap и параметр Swappiness](https://docs.kernel.org/6.12/admin-guide/sysctl/vm.html#swappiness)
- [Политика выделения виртуальной памяти](https://docs.kernel.org/6.12/mm/overcommit-accounting.html)
- [Параметры oom_score и oom_score_adj](https://docs.kernel.org/6.12/filesystems/proc.html)

---
### Исходный код ядра Linux (GitHub)
---

- [Проверка возможности дальнейшего освобождения памяти](https://github.com/torvalds/linux/blob/v6.12/mm/page_alloc.c#L3816-L3894)
- [Переход от Reclaim к OOM-killer](https://github.com/torvalds/linux/blob/v6.12/mm/page_alloc.c#L4091-L4140)
- [Формула расчёта оценки процесса](https://github.com/torvalds/linux/blob/v6.12/mm/oom_kill.c#L181-L226)
- [Учёт общего объёма RAM и Swap](https://github.com/torvalds/linux/blob/v6.12/mm/oom_kill.c#L237-L253)
- [Выбор процесса с максимальной оценкой](https://github.com/torvalds/linux/blob/v6.12/mm/oom_kill.c#L289-L356)
- [Принудительное завершение процесса сигналом](https://github.com/torvalds/linux/blob/v6.12/mm/oom_kill.c#L879-L895)
- [Освобождение памяти OOM-жертвы](https://github.com/torvalds/linux/blob/v6.12/mm/oom_kill.c#L617-L654)

---
### Сборка проекта
---

Рендеринг сцен

```bash
manim -qh scenes/scene_01_normal.py Scene01Normal
manim -qh scenes/scene_02_growth.py Scene02Growth
manim -qh scenes/scene_03_pressure.py Scene03Pressure
manim -qh scenes/scene_04_selection.py Scene04Selection
manim -qh scenes/scene_05_kill.py Scene05Kill
manim -qh scenes/scene_06_recovery.py Scene06Recovery
```

Сборка итогового видео

```bash
ffmpeg -y -f concat -safe 0 -i videos.txt \
    -c copy final_oom_killer.mp4
```
