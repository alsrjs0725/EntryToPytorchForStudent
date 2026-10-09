"""브로드캐스팅으로 (3,) 편향이 (4, 3)의 모든 행에 더해지는 모습을 보여줍니다."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import DOWN, LEFT, RIGHT, UP, FadeIn, FadeOut, LaggedStart, Scene, VGroup, Write

from common.style import COLOR_BIAS, COLOR_INPUT, COLOR_OUTPUT, ko
from common.tensor import code, fmt, grid

BIAS = [1.0, 2.0, 3.0]


class TensorBroadcast(Scene):
    def construct(self):
        title = ko("작은 텐서를 늘려서 모양을 맞춰요", size=32).to_edge(UP)
        self.play(Write(title))

        x = grid([[fmt(0)] * 3 for _ in range(4)], COLOR_INPUT).shift(LEFT * 4 + DOWN * 0.3)
        plus = code("+").next_to(x, RIGHT, buff=0.4)
        bias = grid([[fmt(v) for v in BIAS]], COLOR_BIAS).next_to(plus, RIGHT, buff=0.4).align_to(x, UP)
        x_label = code("x (4, 3)", size=24).next_to(x, DOWN, buff=0.3)
        bias_label = code("bias (3,)", size=24, color=COLOR_BIAS).next_to(bias, UP, buff=0.3)
        self.play(FadeIn(x), FadeIn(x_label), FadeIn(plus), FadeIn(bias), FadeIn(bias_label))
        self.wait(0.5)

        # bias를 아래로 3번 복사해 (4, 3)처럼 만듭니다. 실제로 메모리에 복사하지는 않아요.
        copies = VGroup(*[bias[0].copy() for _ in range(3)])
        stretched = grid([[fmt(v) for v in BIAS] for _ in range(4)], COLOR_BIAS).move_to(bias, aligned_edge=UP)
        for copy in copies:
            copy.set_opacity(0.5)
        step = ko("(3,)을 행마다 복사한 것처럼 (4, 3)으로 늘려요", size=24, color=COLOR_BIAS)
        step.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(step))
        self.play(
            LaggedStart(*[copy.animate.move_to(stretched[k + 1]) for k, copy in enumerate(copies)], lag_ratio=0.3),
            run_time=1.5,
        )
        self.wait(0.5)

        equals = code("=").next_to(stretched, RIGHT, buff=0.4)
        result = grid([[fmt(v) for v in BIAS] for _ in range(4)], COLOR_OUTPUT)
        result.next_to(equals, RIGHT, buff=0.4).align_to(x, UP)
        result_label = code("x + bias (4, 3)", size=24, color=COLOR_OUTPUT).next_to(result, DOWN, buff=0.3)
        self.play(FadeIn(equals))
        self.play(LaggedStart(*[FadeIn(row, shift=RIGHT * 0.3) for row in result], lag_ratio=0.3), FadeIn(result_label))
        summary = code("(4, 3) + (3,) → (4, 3)", color=COLOR_OUTPUT).move_to(step)
        self.play(FadeOut(step), FadeIn(summary))
        self.wait(1.5)
