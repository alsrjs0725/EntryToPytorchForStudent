"""선형 레이어 y = Wx + b가 2차원 공간을 어떻게 바꾸는지 보여줍니다."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import (
    DOWN,
    LEFT,
    UL,
    UP,
    Create,
    Dot,
    FadeIn,
    NumberPlane,
    Scene,
    VGroup,
    Write,
)

from common.style import COLOR_BIAS, COLOR_INPUT, COLOR_OUTPUT, COLOR_WEIGHT, ko

# 선형 레이어의 가중치와 편향. nn.Linear(2, 2)의 weight, bias와 같은 역할입니다.
W = [[1.0, 0.8], [-0.4, 1.2]]
B = [1.0, 0.5]


class LinearLayer(Scene):
    def construct(self):
        title = ko("선형 레이어는 공간을 바꾸는 함수예요", size=34).to_edge(UP)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-6, 6], y_range=[-4, 4], background_line_style={"stroke_opacity": 0.5})
        points = VGroup(
            *[Dot(plane.c2p(x, y), radius=0.06, color=COLOR_INPUT) for x in range(-2, 3) for y in range(-2, 3)]
        )
        self.play(Create(plane), FadeIn(points))
        self.wait(0.5)

        step_w = ko("1. 가중치 W를 곱하면 늘어나고 기울어져요", size=26, color=COLOR_WEIGHT)
        step_w.to_corner(UL).shift(DOWN * 0.8)
        self.play(FadeIn(step_w))
        self.play(plane.animate.apply_matrix(W), points.animate.apply_matrix(W), run_time=2)
        self.wait(0.5)

        step_b = ko("2. 편향 b를 더하면 통째로 이동해요", size=26, color=COLOR_BIAS)
        step_b.next_to(step_w, DOWN, aligned_edge=LEFT)
        shift = plane.c2p(*B) - plane.c2p(0, 0)
        self.play(FadeIn(step_b))
        self.play(plane.animate.shift(shift), points.animate.shift(shift), run_time=1.5)
        self.play(points.animate.set_color(COLOR_OUTPUT))

        summary = ko("y = Wx + b", size=40, color=COLOR_OUTPUT).to_edge(DOWN)
        self.play(Write(summary))
        self.wait(1)
