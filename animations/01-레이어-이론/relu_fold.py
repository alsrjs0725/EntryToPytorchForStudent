"""활성화 함수 ReLU가 선형 레이어를 지난 공간을 접는 모습을 보여줍니다."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
from manim import DOWN, LEFT, UL, UP, Create, Dot, FadeIn, NumberPlane, Scene, VGroup, Write

from common.style import COLOR_BIAS, COLOR_INPUT, COLOR_OUTPUT, COLOR_WEIGHT, ko

# 노트북 01-02와 같은 가중치와 편향입니다.
W = np.array([[1.0, 0.8], [-0.4, 1.2]])
B = np.array([1.0, 0.5])
GRID = [(x, y) for x in np.linspace(-2, 2, 9) for y in np.linspace(-2, 2, 9)]


class ReluFold(Scene):
    def construct(self):
        title = ko("활성화 함수는 공간을 접어요", size=34).to_edge(UP)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-5, 5], y_range=[-4, 4], x_length=8, y_length=6.4, background_line_style={"stroke_opacity": 0.4}
        ).shift(DOWN * 0.4)
        dots = VGroup(*[Dot(plane.c2p(x, y), radius=0.05, color=COLOR_INPUT) for x, y in GRID])
        self.play(Create(plane), FadeIn(dots))

        step1 = ko("1. 선형 레이어: Wx + b", size=24, color=COLOR_WEIGHT).to_corner(UL).shift(DOWN * 0.8)
        self.play(FadeIn(step1))
        hidden = [W @ np.array(p) + B for p in GRID]
        self.play(*[d.animate.move_to(plane.c2p(*h)) for d, h in zip(dots, hidden)], run_time=2)
        self.wait(0.5)

        step2 = ko("2. ReLU: 음수 좌표를 0으로", size=24, color=COLOR_BIAS)
        step2.next_to(step1, DOWN, aligned_edge=LEFT)
        self.play(FadeIn(step2))
        folded = [np.maximum(h, 0) for h in hidden]
        self.play(
            *[d.animate.move_to(plane.c2p(*f)).set_color(COLOR_OUTPUT) for d, f in zip(dots, folded)],
            run_time=2.5,
        )
        self.wait(0.5)

        note = ko("음수였던 좌표가 0이 되어 축 위로 모여요", size=24).next_to(step2, DOWN, aligned_edge=LEFT)
        self.play(FadeIn(note))
        summary = ko("y = ReLU(Wx + b)", size=36, color=COLOR_OUTPUT).to_edge(DOWN)
        self.play(Write(summary))
        self.wait(1.5)
