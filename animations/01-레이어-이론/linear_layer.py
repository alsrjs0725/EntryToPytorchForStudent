"""선형 레이어를 숫자 하나짜리 y = wx + b에서 시작해 2차원 y = Wx + b로 넓혀 보여줍니다."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UL,
    UP,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    NumberLine,
    NumberPlane,
    Scene,
    Text,
    Transform,
    ValueTracker,
    VGroup,
    Write,
    always_redraw,
)

from common.style import COLOR_BIAS, COLOR_INPUT, COLOR_MUTED, COLOR_OUTPUT, COLOR_WEIGHT, ko

# 2차원 선형 레이어의 가중치와 편향. 노트북의 W, b와 같은 값입니다.
W = [[1.0, 0.8], [-0.4, 1.2]]
B = [1.0, 0.5]


def fmt(v: float) -> str:
    return f"{v:.1f}".replace("-0.0", "0.0")


class LinearLayer(Scene):
    def construct(self):
        self.one_dim()
        self.two_dim()

    def one_dim(self):
        """숫자 하나를 받아 숫자 하나를 내는 y = wx + b. w와 b를 바꿔 봅니다."""
        title = ko("숫자 하나부터: y = w·x + b", size=34).to_edge(UP)
        self.play(Write(title))

        top = NumberLine(x_range=[-5, 5, 1], length=11).shift(UP * 1.2)
        bottom = NumberLine(x_range=[-5, 5, 1], length=11).shift(DOWN * 1.6)
        # 눈금 숫자는 LaTeX 없이 Text로 붙입니다.
        for line in (top, bottom):
            line.add(*[Text(str(n), font_size=20).next_to(line.n2p(n), DOWN, buff=0.15) for n in range(-5, 6)])
        top_label = ko("입력 x", size=24, color=COLOR_INPUT).next_to(top, LEFT, buff=0.2)
        bottom_label = ko("출력 y", size=24, color=COLOR_OUTPUT).next_to(bottom, LEFT, buff=0.2)
        VGroup(top, bottom, top_label, bottom_label).shift(RIGHT * 0.4)

        w = ValueTracker(1.0)
        b = ValueTracker(0.0)
        xs = [-2, -1, 0, 1, 2]

        inputs = VGroup(*[Dot(top.n2p(x), radius=0.08, color=COLOR_INPUT) for x in xs])
        outputs = always_redraw(
            lambda: VGroup(
                *[Dot(bottom.n2p(w.get_value() * x + b.get_value()), radius=0.08, color=COLOR_OUTPUT) for x in xs]
            )
        )
        links = always_redraw(
            lambda: VGroup(
                *[
                    Line(top.n2p(x), bottom.n2p(w.get_value() * x + b.get_value()), stroke_width=2, color=COLOR_MUTED)
                    for x in xs
                ]
            )
        )

        def formula():
            parts = VGroup(
                ko("y = ", size=32),
                ko(fmt(w.get_value()), size=32, color=COLOR_WEIGHT),
                ko(" · x + ", size=32),
                ko(fmt(b.get_value()), size=32, color=COLOR_BIAS),
            ).arrange(RIGHT, buff=0.05)
            return parts.move_to(UP * 2.4)

        eq = always_redraw(formula)

        self.play(Create(top), Create(bottom), FadeIn(top_label), FadeIn(bottom_label))
        self.play(FadeIn(inputs), FadeIn(eq), FadeIn(links), FadeIn(outputs))
        caption = ko("w = 1, b = 0이면 그대로예요", size=26).to_edge(DOWN)
        self.play(FadeIn(caption))
        self.wait(0.6)

        steps = [
            ("w가 1보다 크면 늘어나요", 2.0, 0.0),
            ("w가 1보다 작으면 줄어들어요", 0.5, 0.0),
            ("w가 음수면 뒤집혀요", -1.0, 0.0),
            ("b를 더하면 통째로 옮겨져요", 1.0, 1.5),
        ]
        for text, w_to, b_to in steps:
            new_caption = ko(text, size=26, color=COLOR_BIAS if b_to else COLOR_WEIGHT).to_edge(DOWN)
            self.play(Transform(caption, new_caption), run_time=0.4)
            self.play(w.animate.set_value(w_to), b.animate.set_value(b_to), run_time=1.5)
            self.wait(0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])

    def two_dim(self):
        """숫자 2개 (x0, x1)를 받아 숫자 2개 (y0, y1)를 내는 y = Wx + b."""
        background = NumberPlane(
            x_range=[-6, 6], y_range=[-4, 4], background_line_style={"stroke_opacity": 0.15}, axis_config={"stroke_opacity": 0.6}
        )
        plane = NumberPlane(x_range=[-6, 6], y_range=[-4, 4], background_line_style={"stroke_opacity": 0.5})
        axis0 = ko("x0", size=26, color=COLOR_INPUT).move_to(background.c2p(5.6, -0.4))
        axis1 = ko("x1", size=26, color=COLOR_INPUT).move_to(background.c2p(0.45, 3.6))

        points = VGroup(
            *[Dot(plane.c2p(x, y), radius=0.06, color=COLOR_INPUT) for x in range(-2, 3) for y in range(-2, 3)]
        )
        marked = Dot(plane.c2p(1, 1), radius=0.1, color=COLOR_INPUT)
        marked_label = ko("(x0, x1) = (1, 1)", size=22, color=COLOR_INPUT).next_to(marked, RIGHT, buff=0.15)

        title = ko("입력이 숫자 2개인 점 x = (x0, x1)", size=30).to_corner(UL)
        self.play(FadeIn(background), Create(plane), FadeIn(points), FadeIn(marked), Write(title))
        self.play(FadeIn(axis0), FadeIn(axis1), FadeIn(marked_label))
        self.wait(0.8)

        step_w = ko("1. W를 곱하면 늘어나고 기울어져요", size=26, color=COLOR_WEIGHT)
        step_w.next_to(title, DOWN, aligned_edge=LEFT)
        self.play(FadeIn(step_w), FadeOut(marked_label))
        moving = VGroup(plane, points, marked)
        self.play(moving.animate.apply_matrix(W), run_time=2)
        self.wait(0.4)

        step_b = ko("2. b를 더하면 통째로 옮겨져요", size=26, color=COLOR_BIAS)
        step_b.next_to(step_w, DOWN, aligned_edge=LEFT)
        shift = plane.c2p(*B) - plane.c2p(0, 0)
        self.play(FadeIn(step_b))
        self.play(moving.animate.shift(shift), run_time=1.5)

        # 출력 좌표는 같은 축에서 y0, y1로 읽어요. (1, 1)은 (2.8, 1.3)으로 옮겨집니다.
        y0 = W[0][0] * 1 + W[0][1] * 1 + B[0]
        y1 = W[1][0] * 1 + W[1][1] * 1 + B[1]
        out0 = ko("y0", size=26, color=COLOR_OUTPUT).move_to(axis0)
        out1 = ko("y1", size=26, color=COLOR_OUTPUT).move_to(axis1)
        out_label = ko(f"(y0, y1) = ({fmt(y0)}, {fmt(y1)})", size=22, color=COLOR_OUTPUT)
        out_label.next_to(marked, RIGHT, buff=0.15)
        self.play(
            points.animate.set_color(COLOR_OUTPUT),
            marked.animate.set_color(COLOR_OUTPUT),
            Transform(axis0, out0),
            Transform(axis1, out1),
            FadeIn(out_label),
        )
        self.wait(0.8)

        # 숫자 하나짜리 식 w·x + b가 출력마다 하나씩 생겨요.
        rows = VGroup(
            ko(f"y0 = {fmt(W[0][0])}·x0 + {fmt(W[0][1])}·x1 + {fmt(B[0])}", size=26),
            ko(f"y1 = {fmt(W[1][0])}·x0 + {fmt(W[1][1])}·x1 + {fmt(B[1])}", size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        rows.to_edge(DOWN).shift(LEFT * 3)
        self.play(FadeIn(rows))
        self.wait(1.5)

        summary = ko("y = Wx + b", size=40, color=COLOR_OUTPUT).move_to(rows)
        self.play(Transform(rows, summary))
        self.wait(1.2)
