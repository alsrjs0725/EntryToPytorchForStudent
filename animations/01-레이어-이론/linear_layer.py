"""선형 레이어를 숫자 하나짜리 y = wx + b에서 시작해 2차원 y = Wx + b로 넓혀 보여줍니다."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import (
    BLACK,
    Arrow,
    GrowArrow,
    Rectangle,
    SurroundingRectangle,
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

from common.style import COLOR_BIAS, COLOR_INPUT, COLOR_MUTED, COLOR_OUTPUT, COLOR_TEXT, COLOR_WEIGHT, ko

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
        """숫자 2개 (x0, x1)를 받아 숫자 2개 (y0, y1)를 내는 y = Wx + b. 슬라이더로 W, b를 하나씩 바꿔 봅니다."""
        w00, w01, w10, w11 = (ValueTracker(v) for v in (1.0, 0.0, 0.0, 1.0))
        b0, b1 = ValueTracker(0.0), ValueTracker(0.0)

        def f(p0, p1):
            """입력 점 (x0, x1)을 출력 점 (y0, y1)로 옮깁니다."""
            return (
                w00.get_value() * p0 + w01.get_value() * p1 + b0.get_value(),
                w10.get_value() * p0 + w11.get_value() * p1 + b1.get_value(),
            )

        # 왼쪽: 평면. 흐린 격자는 입력 공간, 노란 격자는 레이어를 지난 출력 공간이에요.
        plane = NumberPlane(
            x_range=[-3, 3],
            y_range=[-3, 3],
            x_length=6.8,
            y_length=6.8,
            background_line_style={"stroke_opacity": 0.25},
            axis_config={"stroke_opacity": 0.7},
        ).to_edge(LEFT, buff=0.3).shift(DOWN * 0.35)
        axis0 = ko("x0 · y0", size=20).move_to(plane.c2p(2.5, -0.3))
        axis1 = ko("x1 · y1", size=20).move_to(plane.c2p(-0.6, 2.75))

        def warped_grid():
            lines = VGroup()
            for v in range(-2, 3):
                for a, b in (((-2, v), (2, v)), ((v, -2), (v, 2))):
                    lines.add(Line(plane.c2p(*f(*a)), plane.c2p(*f(*b)), color=COLOR_OUTPUT, stroke_width=2, stroke_opacity=0.55))
            return lines

        grid_out = always_redraw(warped_grid)
        x_arrow = Arrow(plane.c2p(0, 0), plane.c2p(1, 1), buff=0, color=COLOR_INPUT, stroke_width=7, tip_length=0.25, max_tip_length_to_length_ratio=0.3)
        x_arrow.set_z_index(1.2)
        x_label = ko("x = (1, 1)", size=22, color=COLOR_INPUT).next_to(x_arrow, LEFT, buff=0.1)
        y_arrow = always_redraw(
            lambda: Arrow(
                plane.c2p(0, 0), plane.c2p(*f(1, 1)), buff=0, color=COLOR_OUTPUT,
                stroke_width=7, tip_length=0.25, max_tip_length_to_length_ratio=0.3,
            ).set_z_index(1.2)
        )
        y_label = always_redraw(
            lambda: ko(f"y = ({fmt(f(1, 1)[0])}, {fmt(f(1, 1)[1])})", size=22, color=COLOR_OUTPUT).next_to(
                plane.c2p(*f(1, 1)), UP, buff=0.1
            )
        )

        # 오른쪽: 식, W와 b의 값, 슬라이더. 격자가 넘어와도 가리도록 불투명한 판을 깝니다.
        panel = Rectangle(width=6.2, height=8.2, fill_color=BLACK, fill_opacity=1, stroke_width=0)
        panel.to_edge(RIGHT, buff=0).set_z_index(0.5)
        cx = panel.get_center()[0]
        eq = VGroup(
            ko("y = ", size=40, color=COLOR_OUTPUT),
            ko("W", size=40, color=COLOR_WEIGHT),
            ko("x", size=40, color=COLOR_INPUT),
            ko(" + ", size=40),
            ko("b", size=40, color=COLOR_BIAS),
        ).arrange(RIGHT, buff=0.05).move_to([cx, 3.3, 0])

        def matrix_view():
            def num(v, color):
                return ko(fmt(v), size=26, color=color)

            cells = VGroup(
                num(w00.get_value(), COLOR_WEIGHT).move_to([cx - 1.9, 2.25, 0]),
                num(w01.get_value(), COLOR_WEIGHT).move_to([cx - 0.9, 2.25, 0]),
                num(w10.get_value(), COLOR_WEIGHT).move_to([cx - 1.9, 1.75, 0]),
                num(w11.get_value(), COLOR_WEIGHT).move_to([cx - 0.9, 1.75, 0]),
                num(b0.get_value(), COLOR_BIAS).move_to([cx + 1.9, 2.25, 0]),
                num(b1.get_value(), COLOR_BIAS).move_to([cx + 1.9, 1.75, 0]),
            )
            return cells.set_z_index(2)

        def brackets(left, right):
            group = VGroup()
            for x, sign in ((left, 1), (right, -1)):
                group.add(
                    Line([x, 2.5, 0], [x, 1.5, 0], stroke_width=2),
                    Line([x, 2.5, 0], [x + 0.12 * sign, 2.5, 0], stroke_width=2),
                    Line([x, 1.5, 0], [x + 0.12 * sign, 1.5, 0], stroke_width=2),
                )
            return group

        matrix_frame = VGroup(
            ko("W =", size=26, color=COLOR_WEIGHT).move_to([cx - 2.85, 2.0, 0]),
            brackets(cx - 2.4, cx - 0.4),
            ko("b =", size=26, color=COLOR_BIAS).move_to([cx + 0.95, 2.0, 0]),
            brackets(cx + 1.45, cx + 2.35),
        ).set_z_index(2)
        matrix = always_redraw(matrix_view)

        slider_specs = [("W00", w00, COLOR_WEIGHT), ("W01", w01, COLOR_WEIGHT), ("W10", w10, COLOR_WEIGHT),
                        ("W11", w11, COLOR_WEIGHT), ("b0", b0, COLOR_BIAS), ("b1", b1, COLOR_BIAS)]
        sliders = VGroup()
        knobs = VGroup()
        for i, (name, tracker, color) in enumerate(slider_specs):
            y = 0.8 - i * 0.62
            track = NumberLine(x_range=[-2, 2, 1], length=3.2, stroke_width=2, tick_size=0.05).move_to([cx + 0.3, y, 0])
            label = ko(name, size=24, color=color).next_to(track, LEFT, buff=0.35)
            sliders.add(VGroup(track, label))
            knobs.add(always_redraw(lambda t=track, tr=tracker, c=color: Dot(t.n2p(tr.get_value()), radius=0.11, color=c).set_z_index(3)))
        sliders.set_z_index(2)
        scale = VGroup(
            Text("-2", font_size=18).next_to(sliders[-1][0].n2p(-2), DOWN, buff=0.15),
            Text("0", font_size=18).next_to(sliders[-1][0].n2p(0), DOWN, buff=0.15),
            Text("2", font_size=18).next_to(sliders[-1][0].n2p(2), DOWN, buff=0.15),
        ).set_z_index(2)

        caption = ko("W00 = W11 = 1, 나머지가 0이면 그대로예요", size=24).move_to([cx, -3.65, 0]).set_z_index(2)

        title = ko("입력이 숫자 2개: x = (x0, x1)", size=28).to_corner(UL, buff=0.25)
        self.play(FadeIn(plane), FadeIn(axis0), FadeIn(axis1), Write(title))
        self.play(GrowArrow(x_arrow), FadeIn(x_label))
        self.play(FadeIn(panel), Write(eq))
        self.play(FadeIn(matrix_frame), FadeIn(matrix), FadeIn(sliders), FadeIn(scale), FadeIn(knobs))
        self.play(FadeIn(grid_out), FadeIn(y_arrow), FadeIn(y_label), FadeIn(caption))
        self.wait(0.8)

        focus = SurroundingRectangle(sliders[0], color=COLOR_TEXT, buff=0.12, stroke_width=2).set_z_index(2)
        self.play(FadeIn(focus), run_time=0.3)

        def step(text, index, changes, back=None, color=COLOR_WEIGHT):
            """슬라이더 하나(또는 여러 개)를 움직였다가 되돌립니다."""
            new_caption = ko(text, size=24, color=color).move_to(caption).set_z_index(2)
            target = SurroundingRectangle(
                VGroup(*[sliders[i] for i in index]), color=COLOR_TEXT, buff=0.12, stroke_width=2
            ).set_z_index(2)
            self.play(Transform(caption, new_caption), Transform(focus, target), run_time=0.5)
            self.play(*[tr.animate.set_value(v) for tr, v in changes], run_time=1.4)
            self.wait(0.5)
            if back:
                self.play(*[tr.animate.set_value(v) for tr, v in back], run_time=0.8)

        step("W00을 키우면 x0 방향으로 늘어나요", [0], [(w00, 2.0)], back=[(w00, 1.0)])
        step("W11을 줄이면 x1 방향으로 줄어들어요", [3], [(w11, 0.5)], back=[(w11, 1.0)])
        step("W01을 바꾸면 옆으로 기울어져요", [1], [(w01, 1.0)], back=[(w01, 0.0)])
        step("W10을 바꾸면 위아래로 기울어져요", [2], [(w10, 1.0)], back=[(w10, 0.0)])
        step("W00이 음수면 좌우가 뒤집혀요", [0], [(w00, -1.0)], back=[(w00, 1.0)])
        step(
            "네 값을 함께 바꾸면 회전도 돼요",
            [0, 1, 2, 3],
            [(w00, 0.7), (w01, -0.7), (w10, 0.7), (w11, 0.7)],
            back=[(w00, 1.0), (w01, 0.0), (w10, 0.0), (w11, 1.0)],
        )
        step("b0을 바꾸면 x0 방향으로 통째로 옮겨져요", [4], [(b0, 1.5)], back=None, color=COLOR_BIAS)
        step("b1을 바꾸면 x1 방향으로 통째로 옮겨져요", [5], [(b1, 1.0)], back=[(b0, 0.0), (b1, 0.0)], color=COLOR_BIAS)

        # 마지막으로 노트북의 W, b를 넣어요. x = (1, 1)은 y = (2.8, 1.3)이 됩니다.
        step(
            "노트북의 W, b를 넣으면 이렇게 바뀌어요",
            [0, 1, 2, 3, 4, 5],
            [(w00, W[0][0]), (w01, W[0][1]), (w10, W[1][0]), (w11, W[1][1]), (b0, B[0]), (b1, B[1])],
            back=None,
            color=COLOR_OUTPUT,
        )
        self.play(FadeOut(focus))
        self.wait(1.5)
