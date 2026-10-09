"""sum(dim=...)이 그 축을 따라 더하고 축을 없애는 모습을 보여줍니다."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    FadeIn,
    FadeOut,
    ReplacementTransform,
    Scene,
    Transform,
    VGroup,
    Write,
)

from common.style import COLOR_INPUT, COLOR_MUTED, COLOR_OUTPUT, ko
from common.tensor import cell, code, grid, highlight

X = [[1, 2], [3, 4]]


class TensorSum(Scene):
    def construct(self):
        title = ko("sum(dim=0)은 0번 축을 따라 더하고, 그 축은 사라져요", size=30).to_edge(UP)
        self.play(Write(title))

        x = grid(X, size=0.9).shift(LEFT * 2.5)
        dim0 = Arrow(x.get_corner(UP + LEFT), x.get_corner(DOWN + LEFT), buff=0, color=COLOR_MUTED).shift(LEFT * 0.4)
        dim1 = Arrow(x.get_corner(UP + LEFT), x.get_corner(UP + RIGHT), buff=0, color=COLOR_MUTED).shift(UP * 0.4)
        dim0_label = code("dim 0", size=22, color=COLOR_MUTED).next_to(dim0, LEFT, buff=0.15)
        dim1_label = code("dim 1", size=22, color=COLOR_MUTED).next_to(dim1, UP, buff=0.15)
        name = code("x  # (2, 2)", size=24).next_to(x, DOWN, buff=0.4)
        self.play(FadeIn(x), FadeIn(VGroup(dim0, dim1, dim0_label, dim1_label, name)))
        self.wait(0.5)

        label = code("x.sum(dim=0)   # (2,)").to_edge(DOWN, buff=0.6)
        steps = [
            # (코드, 강조할 축, 결과 칸 j에 모이는 칸들)
            ("x.sum(dim=0)   # (2,)", VGroup(dim0, dim0_label), [[(0, j), (1, j)] for j in range(2)]),
            ("x.sum(dim=1)   # (2,)", VGroup(dim1, dim1_label), [[(i, 0), (i, 1)] for i in range(2)]),
        ]
        for k, (text, axis, groups) in enumerate(steps):
            if k == 0:
                self.play(Write(label))
            else:
                new_title = ko("sum(dim=1)은 1번 축을 따라 더하고, 그 축은 사라져요", size=30).move_to(title)
                self.play(Transform(label, code(text).move_to(label)), Transform(title, new_title))
            self.play(axis.animate.set_color(COLOR_OUTPUT))

            result = VGroup(
                *[cell(sum(X[i][j] for i, j in g), COLOR_OUTPUT, size=0.9) for g in groups]
            ).arrange(RIGHT, buff=0).shift(RIGHT * 2.8)
            shape_text = code("(2,)", size=26, color=COLOR_OUTPUT).next_to(result, DOWN, buff=0.3)
            for g, target in zip(groups, result):
                copies = VGroup(*[x[i][j].copy() for i, j in g])
                self.play(*[highlight(x[i][j], COLOR_OUTPUT, opacity=0.5) for i, j in g], run_time=0.5)
                self.play(ReplacementTransform(copies, target), run_time=1)
                self.play(*[highlight(x[i][j], COLOR_INPUT, opacity=0.25) for i, j in g], run_time=0.3)
            self.play(FadeIn(shape_text))
            self.wait(1.2)
            self.play(FadeOut(result), FadeOut(shape_text), axis.animate.set_color(COLOR_MUTED))
        self.wait(0.5)
