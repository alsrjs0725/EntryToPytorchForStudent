"""reshape가 값의 순서는 그대로 두고 모양만 바꾸는 모습을 보여줍니다."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import DOWN, RIGHT, UP, FadeIn, Indicate, LaggedStart, Scene, Transform, VGroup, Write

from common.style import COLOR_OUTPUT, ko
from common.tensor import cell, code


class TensorReshape(Scene):
    def construct(self):
        title = ko("reshape는 순서를 그대로 두고 모양만 바꿔요", size=32).to_edge(UP)
        self.play(Write(title))

        # torch.arange(12)의 값 0~11
        cells = VGroup(*[cell(i) for i in range(12)]).arrange(RIGHT, buff=0)
        label = code("x = torch.arange(12)   # (12,)").to_edge(DOWN, buff=0.8)
        self.play(FadeIn(cells), Write(label))
        self.wait(1)

        for rows, cols, text in [(3, 4, "x.reshape(3, 4)    # (3, 4)"), (4, 3, "x.reshape(4, -1)   # (4, 3)")]:
            # 같은 크기의 빈 칸을 격자로 놓아 목표 위치를 구합니다. 행 우선으로 채워집니다.
            target = VGroup(*[cell() for _ in range(12)]).arrange_in_grid(rows=rows, cols=cols, buff=0)
            target.move_to(UP * 0.3)
            new_label = code(text).move_to(label)
            self.play(
                *[c.animate.move_to(t) for c, t in zip(cells, target)],
                Transform(label, new_label),
                run_time=2,
            )
            self.wait(1)

        note = ko("값은 0부터 11까지 같은 순서로 채워져요", size=26, color=COLOR_OUTPUT)
        note.next_to(label, UP, buff=0.3)
        self.play(FadeIn(note))
        self.play(LaggedStart(*[Indicate(c, color=COLOR_OUTPUT) for c in cells], lag_ratio=0.15))
        self.wait(1)
