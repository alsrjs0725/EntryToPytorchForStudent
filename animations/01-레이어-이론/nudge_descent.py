"""w, b를 하나씩 조금 늘려 보고 줄여 봐서 손실이 줄어드는 방향(↑/↓)을 찾고, lr만큼 옮기기를 되풀이합니다."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Axes,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    Line,
    NumberLine,
    Scene,
    SurroundingRectangle,
    Text,
    Transform,
    ValueTracker,
    VGroup,
    always_redraw,
)

from common.style import (
    COLOR_BIAS,
    COLOR_GRAD,
    COLOR_INPUT,
    COLOR_LOSS,
    COLOR_MUTED,
    COLOR_OUTPUT,
    COLOR_TEXT,
    COLOR_WEIGHT,
    ko,
)
from common.tensor import code

# 노트북 01-03과 같은 데이터: torch.manual_seed(0) 뒤 y = 2x + 1 + 0.3 * randn(30)
X = np.linspace(-1, 1, 30)
Y = np.array([
    -1.338, -1.208, -0.799, -0.716, -0.194, -0.103, -0.267, -0.669, 0.2, -0.138,
    0.484, 0.61, 0.691, 1.164, 0.888, 1.035, 1.023, 1.354, 1.335, 1.695,
    1.891, 1.93, 1.782, 1.478, 2.28, 2.686, 2.499, 2.74, 3.019, 3.691,
])
W0, B0 = 0.5, 0.0  # 시작점
NUDGE = 0.1  # 조금 늘리고 줄여 보는 크기
LR = 0.1
STEPS = 50


def mse(w, b):
    return float(np.mean((w * X + b - Y) ** 2))


def grads(w, b):
    """손실을 w, b로 미분한 값. 영상 속 PyTorch의 w.grad, b.grad와 같습니다."""
    err = w * X + b - Y
    return float(np.mean(2 * err * X)), float(np.mean(2 * err))


def history():
    w, b = W0, B0
    path = [(w, b)]
    for _ in range(STEPS - 1):
        gw, gb = grads(w, b)
        w, b = w - LR * gw, b - LR * gb
        path.append((w, b))
    return path


def f2(v):
    return f"{v:.2f}".replace("-0.00", "0.00")


def direction_arrow(point, up: bool, length=0.55):
    start = point + (DOWN if up else UP) * length / 2
    end = point + (UP if up else DOWN) * length / 2
    return Arrow(start, end, buff=0, color=COLOR_GRAD, stroke_width=8,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=20).set_z_index(2)


class NudgeDescent(Scene):
    def construct(self):
        w = ValueTracker(W0)
        b = ValueTracker(B0)

        # 왼쪽: 데이터와 지금의 직선
        axes = Axes(
            x_range=[-1.2, 1.2, 0.5],
            y_range=[-2, 4, 1],
            x_length=6.0,
            y_length=6.2,
            tips=False,
            axis_config={"stroke_opacity": 0.6},
        ).to_edge(LEFT, buff=0.5).shift(UP * 0.35)
        ticks = VGroup(
            *[Text(str(n), font_size=18, color=COLOR_MUTED).next_to(axes.c2p(n, 0), DOWN, buff=0.12) for n in (-1, 1)],
            *[Text(str(n), font_size=18, color=COLOR_MUTED).next_to(axes.c2p(0, n), LEFT, buff=0.12) for n in (-2, 2, 4)],
        )
        dots = VGroup(*[Dot(axes.c2p(x, y), radius=0.06, color=COLOR_INPUT) for x, y in zip(X, Y)])
        line = always_redraw(
            lambda: Line(
                axes.c2p(-1.2, w.get_value() * -1.2 + b.get_value()),
                axes.c2p(1.2, w.get_value() * 1.2 + b.get_value()),
                color=COLOR_OUTPUT,
                stroke_width=5,
            )
        )

        # 오른쪽: 식, 손실, w와 b 슬라이더
        cx = 3.7

        def formula():
            return VGroup(
                ko("y = ", size=34, color=COLOR_OUTPUT),
                ko(f2(w.get_value()), size=34, color=COLOR_WEIGHT),
                ko(" · x + ", size=34),
                ko(f2(b.get_value()), size=34, color=COLOR_BIAS),
            ).arrange(RIGHT, buff=0.05).move_to([cx, 3.2, 0])

        eq = always_redraw(formula)
        loss_text = always_redraw(
            lambda: ko(f"손실 {mse(w.get_value(), b.get_value()):.3f}", size=34, color=COLOR_LOSS).move_to([cx, 2.35, 0])
        )

        rows = {}
        for name, tracker, color, y in (("w", w, COLOR_WEIGHT, 1.25), ("b", b, COLOR_BIAS, 0.2)):
            track = NumberLine(x_range=[-1, 3, 1], length=3.4, stroke_width=2, tick_size=0.05).move_to([cx - 0.3, y, 0])
            label = ko(name, size=30, color=color).next_to(track, LEFT, buff=0.3)
            scale = VGroup(*[Text(str(n), font_size=16, color=COLOR_MUTED).next_to(track.n2p(n), DOWN, buff=0.12)
                             for n in (-1, 0, 1, 2, 3)])
            knob = always_redraw(lambda t=track, tr=tracker, c=color: Dot(t.n2p(tr.get_value()), radius=0.12, color=c).set_z_index(1))
            slot = track.get_right() + RIGHT * 0.55
            rows[name] = {"group": VGroup(label, track, scale), "knob": knob, "slot": slot}

        caption = ko("데이터에 맞는 직선 y = w·x + b를 찾고 싶어요", size=26).to_edge(DOWN, buff=0.3)

        def say(text, color=COLOR_TEXT, run_time=0.4):
            self.play(Transform(caption, ko(text, size=26, color=color).move_to(caption)), run_time=run_time)

        self.play(Create(axes), FadeIn(ticks), FadeIn(dots), FadeIn(caption))
        self.play(FadeIn(line), FadeIn(eq), FadeIn(loss_text))
        self.play(*[FadeIn(r["group"]) for r in rows.values()], *[FadeIn(r["knob"]) for r in rows.values()])
        say("w = 0.5, b = 0에서 시작해요. 손실은 1.946이에요")
        self.wait(1.0)

        # 1. w, b를 하나씩 조금 늘려 보고 줄여 봐요.
        arrows = {}
        for name, tracker, start in (("w", w, W0), ("b", b, B0)):
            fast = name == "b"
            focus = SurroundingRectangle(rows[name]["group"], color=COLOR_TEXT, buff=0.12, stroke_width=2)
            self.play(FadeIn(focus), run_time=0.3)
            tries = VGroup()
            for sign, verb in ((1, "늘려"), (-1, "줄여")):
                if not fast:
                    say(f"{name}를 {NUDGE}만큼 {verb} 봐요")
                value = start + sign * NUDGE
                self.play(tracker.animate.set_value(value), run_time=0.6 if fast else 1.0)
                pw, pb = (value, B0) if name == "w" else (W0, value)
                note = ko(f"{name} {'+' if sign > 0 else '−'} {NUDGE} → 손실 {mse(pw, pb):.3f}", size=24)
                note.move_to([cx, -1.1 - 0.6 * len(tries), 0])
                self.play(FadeIn(note), run_time=0.3)
                tries.add(note)
                self.play(tracker.animate.set_value(start), run_time=0.4 if fast else 0.6)

            up = mse(*((start + NUDGE, B0) if name == "w" else (W0, start + NUDGE))) < mse(
                *((start - NUDGE, B0) if name == "w" else (W0, start - NUDGE))
            )
            winner = tries[0] if up else tries[1]
            arrows[name] = direction_arrow(rows[name]["slot"], up)
            say(f"{'늘렸을' if up else '줄였을'} 때 손실이 줄었어요. {name}는 {'↑' if up else '↓'} 방향이에요", color=COLOR_GRAD)
            self.play(winner.animate.set_color(COLOR_GRAD), FadeIn(arrows[name], shift=UP * 0.2 if up else DOWN * 0.2))
            self.wait(0.8)
            self.play(FadeOut(tries), FadeOut(focus), run_time=0.4)

        # 2. 실제로는 미분으로 방향을 한 번에 구해요.
        gw, gb = grads(W0, B0)
        say("실제로는 하나씩 해 보지 않고, 미분으로 방향을 한 번에 구해요")
        backward = VGroup(
            code("loss.backward()", size=24),
            code(f"w.grad = {gw:.2f}", size=24, color=COLOR_WEIGHT),
            code(f"b.grad = {gb:.2f}", size=24, color=COLOR_BIAS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([cx, -1.6, 0])
        self.play(FadeIn(backward))
        self.wait(1.0)
        say("기울기가 음수면 늘리는 쪽(↑)이 내리막이에요", color=COLOR_GRAD)
        self.play(Indicate(arrows["w"], color=COLOR_GRAD), Indicate(arrows["b"], color=COLOR_GRAD))
        self.wait(1.0)

        # 3. 화살표 방향으로 lr × 기울기만큼 옮겨요.
        path = history()
        w1, b1 = path[1]
        say(f"화살표 방향으로 lr × 기울기만큼 옮겨요 (lr = {LR})")
        update = VGroup(
            ko(f"w: {f2(W0)} − {LR} × ({gw:.2f}) = {f2(w1)}", size=24, color=COLOR_WEIGHT),
            ko(f"b: {f2(B0)} − {LR} × ({gb:.2f}) = {f2(b1)}", size=24, color=COLOR_BIAS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(backward)
        self.play(FadeOut(backward), FadeIn(update))
        self.wait(1.2)
        self.play(w.animate.set_value(w1), b.animate.set_value(b1), run_time=1.5)
        self.wait(0.8)

        # 4. 되풀이: 매번 방향을 다시 구하고 lr만큼 옮겨요.
        def live_arrow(name):
            def make():
                gw_, gb_ = grads(w.get_value(), b.get_value())
                g = gw_ if name == "w" else gb_
                return direction_arrow(rows[name]["slot"], g < 0)
            return always_redraw(make)

        self.remove(arrows["w"], arrows["b"])
        live = [live_arrow("w"), live_arrow("b")]
        self.add(*live)
        step = ValueTracker(1)
        counter = always_redraw(lambda: ko(f"step {int(round(step.get_value()))}", size=28).move_to([cx, -1.6, 0]))
        self.play(FadeOut(update), FadeIn(counter), run_time=0.4)
        say("이 과정을 되풀이해요. 방향을 구하고, lr만큼 옮기고")
        for i, (wi, bi) in enumerate(path[2:], start=2):
            run_time = 0.6 if i < 6 else 0.12
            self.play(w.animate.set_value(wi), b.animate.set_value(bi), step.animate.set_value(i), run_time=run_time)
        w_end, b_end = path[-1]
        say(f"w = {f2(w_end)}, b = {f2(b_end)}, 손실 {mse(w_end, b_end):.3f}. 바닥 근처에 왔어요", color=COLOR_OUTPUT)
        self.wait(2.5)
