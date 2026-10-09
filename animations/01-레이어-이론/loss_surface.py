"""loss vs w 곡선을 b마다 그려 쌓고, 그 사이를 메워 loss over (w, b) 곡면을 만듭니다."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
from manim import (
    DEGREES,
    DOWN,
    RIGHT,
    UR,
    Create,
    Dot3D,
    FadeIn,
    FadeOut,
    ParametricFunction,
    Surface,
    Text,
    ThreeDAxes,
    ThreeDScene,
    VGroup,
)

from common.style import COLOR_BIAS, COLOR_LOSS, COLOR_MUTED, COLOR_OUTPUT, COLOR_TEXT, COLOR_WEIGHT, ko

# 노트북 01-03과 같은 데이터: torch.manual_seed(0) 뒤 y = 2x + 1 + 0.3 * randn(30)
X = np.linspace(-1, 1, 30)
Y = np.array([
    -1.338, -1.208, -0.799, -0.716, -0.194, -0.103, -0.267, -0.669, 0.2, -0.138,
    0.484, 0.61, 0.691, 1.164, 0.888, 1.035, 1.023, 1.354, 1.335, 1.695,
    1.891, 1.93, 1.782, 1.478, 2.28, 2.686, 2.499, 2.74, 3.019, 3.691,
])
W_RANGE = (-1, 5)  # 문서 그림과 같은 범위
B_RANGE = (-2, 4)
B_STEPS = np.arange(-2, 4.01, 0.5)  # 곡선을 그릴 b 값 13개


def mse(w, b):
    return float(np.mean((w * X + b - Y) ** 2))


class LossSurface(ThreeDScene):
    def construct(self):
        # 축의 원점을 (w, b) = (-1, -2) 모서리에 두려고 w + 1, b + 2를 그립니다. 눈금 글자는 실제 값으로 적어요.
        axes = ThreeDAxes(
            x_range=[0, 6, 1], y_range=[0, 6, 1], z_range=[0, 13, 4],
            x_length=6, y_length=6, z_length=4,
            axis_config={"stroke_opacity": 0.7},
        )
        axes.shift(-axes.c2p(3, 3, 6.5))  # 곡면 한가운데가 화면 가운데에 오도록

        def p(w, b, loss):
            return axes.c2p(w - W_RANGE[0], b - B_RANGE[0], loss)

        def standing(text, size, color, at):
            """세워 둔 글자. 정면과 비스듬한 시점에서 읽혀요."""
            return Text(text, font_size=size, color=color).rotate(90 * DEGREES, RIGHT).move_to(at)

        def lying(text, size, color, at):
            """눕혀 둔 글자. 위에서 내려다볼 때 읽혀요."""
            return Text(text, font_size=size, color=color).move_to(at)

        w_labels = VGroup(
            *[standing(str(n), 24, COLOR_MUTED, p(n, B_RANGE[0], -0.9)) for n in range(-1, 6)],
            standing("w", 32, COLOR_WEIGHT, p(5.6, B_RANGE[0], 0)),
        )
        loss_labels = VGroup(
            *[standing(str(n), 24, COLOR_MUTED, p(W_RANGE[0] - 0.35, B_RANGE[0], n)) for n in (4, 8, 12)],
            standing("손실", 28, COLOR_LOSS, p(W_RANGE[0], B_RANGE[0], 14.8)),
        )
        b_labels = VGroup(
            *[standing(str(n), 24, COLOR_MUTED, p(W_RANGE[0] - 0.4, n, -0.9)) for n in (-2, 0, 2, 4)],
            standing("b", 32, COLOR_BIAS, p(W_RANGE[0] - 0.4, 4.7, 0)),
        )

        def curve(b, opacity=1.0, width=4):
            return ParametricFunction(
                lambda t: p(t, b, mse(t, b)), t_range=[W_RANGE[0], W_RANGE[1]],
                color=COLOR_LOSS, stroke_width=width, stroke_opacity=opacity,
            )

        # 화면에 고정된 글자(자막, b 값)는 바꿀 때마다 새로 만들어 갈아 끼워요. Transform을 쓰면 글자 일부가 3차원 공간으로 빠져요.
        fixed = {}

        def swap(key, mob):
            self.add_fixed_in_frame_mobjects(mob)
            self.remove(mob)
            old = fixed.get(key)
            fixed[key] = mob
            return [FadeIn(mob)] + ([FadeOut(old)] if old is not None else [])

        def say(text, color=COLOR_TEXT):
            return swap("caption", ko(text, size=26, color=color).to_edge(DOWN, buff=0.3))

        def show_b(b):
            return swap("tag", ko(f"b = {b:.1f}", size=30, color=COLOR_BIAS).to_corner(UR, buff=0.4))

        # 1. 정면에서 본 loss vs w (b = 1)
        # focal_distance를 크게 두면 원근이 거의 사라져서, 깊이가 다른 곡선도 같은 크기로 보여요.
        self.set_camera_orientation(phi=90 * DEGREES, theta=-90 * DEGREES, zoom=1.0, focal_distance=200)
        self.play(Create(axes.x_axis), Create(axes.z_axis), FadeIn(w_labels), FadeIn(loss_labels),
                  *say("b = 1로 두고 w만 바꾸면 손실은 이런 곡선이에요"))
        first = curve(1.0)
        self.play(Create(first), *show_b(1.0), run_time=1.5)
        self.wait(1.0)

        # 2. b를 바꿔 가며 계속 그려요. 정면에서는 곡선이 한 평면에 겹쳐 보여요.
        self.play(*say("b를 바꿔 가며 계속 그려 봐요"), first.animate.set_stroke(opacity=0.35, width=2), run_time=0.5)
        curves = VGroup()
        for b in B_STEPS:
            c = curve(b)
            self.play(Create(c), *show_b(b), run_time=0.45)
            self.play(c.animate.set_stroke(opacity=0.45, width=2.5), run_time=0.15)
            curves.add(c)
        self.remove(first)  # b = 1 곡선은 curves 안에도 있어요
        self.wait(0.5)

        # 3. 돌려 보면 곡선마다 b 자리에 놓여 있어요. 이미지를 쌓듯 b 순서대로 쌓인 거예요.
        self.play(*say("돌려 보면 곡선이 b 순서대로 쌓여 있어요"), FadeOut(fixed.pop("tag")), run_time=0.5)
        self.move_camera(phi=68 * DEGREES, theta=-50 * DEGREES, zoom=0.85, added_anims=[Create(axes.y_axis), FadeIn(b_labels)], run_time=3)
        self.play(curves.animate.set_stroke(opacity=1.0, width=3), run_time=0.6)
        self.wait(0.8)

        # 4. 곡선 사이를 메우면 곡면이 돼요.
        surface = Surface(
            lambda u, v: p(u, v, mse(u, v)),
            u_range=W_RANGE, v_range=B_RANGE, resolution=(30, 30),
            fill_opacity=0.75, stroke_width=0.3, stroke_color=COLOR_MUTED, checkerboard_colors=False,
        )
        surface.set_fill_by_value(axes=axes, colorscale=[("#FDE2D8", 0), ("#F08A6B", 4), ("#C0392B", 12)], axis=2)
        self.play(*say("곡선 사이를 메우면 손실 곡면 loss over (w, b)가 돼요"), FadeIn(surface), curves.animate.set_stroke(opacity=0.6, width=2), run_time=2)
        self.begin_ambient_camera_rotation(rate=0.12)
        self.wait(3)
        self.stop_ambient_camera_rotation()

        # 5. 가장 낮은 곳: 손실이 가장 작은 (w, b)
        w_best, b_best = np.linalg.lstsq(np.vstack([X, np.ones_like(X)]).T, Y, rcond=None)[0]
        bottom = Dot3D(p(w_best, b_best, mse(w_best, b_best)), radius=0.1, color=COLOR_OUTPUT)
        self.play(
            *say(f"가장 낮은 곳이 손실이 가장 작은 w = {w_best:.2f}, b = {b_best:.2f}예요", color=COLOR_OUTPUT),
            FadeIn(bottom), run_time=1,
        )
        self.wait(1.2)

        # 6. 위에서 내려다보면 문서의 손실 지도와 같아요.
        flat = VGroup(
            *[lying(str(n), 24, COLOR_MUTED, p(n, B_RANGE[0] - 0.35, 0)) for n in range(-1, 6)],
            lying("w", 30, COLOR_WEIGHT, p(5.5, B_RANGE[0] - 0.35, 0)),
            *[lying(str(n), 24, COLOR_MUTED, p(W_RANGE[0] - 0.35, n, 0)) for n in (-2, 0, 2, 4)],
            lying("b", 30, COLOR_BIAS, p(W_RANGE[0] - 0.35, 4.5, 0)),
        )
        self.play(*say("위에서 내려다보면 색이 옅을수록 손실이 작은 지도가 돼요"), run_time=0.5)
        self.move_camera(
            phi=0, theta=-90 * DEGREES, zoom=0.85,
            added_anims=[FadeOut(w_labels), FadeOut(b_labels), FadeOut(loss_labels), FadeOut(axes.z_axis), FadeIn(flat)],
            run_time=3,
        )
        self.wait(2.5)
