"""행렬 곱 (4, 3) @ (3, 2)에서 결과 한 칸이 어떻게 만들어지는지 보여줍니다."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import DOWN, LEFT, RIGHT, UP, FadeIn, LaggedStart, Scene, Text, VGroup, Write

from common.style import COLOR_INPUT, COLOR_OUTPUT, COLOR_WEIGHT, ko
from common.tensor import MONO_FONT, code, grid, highlight

SIZE = 0.6


def shape_label(text: str) -> Text:
    # 모양에서 맞아야 하는 크기 3만 강조합니다.
    return Text(text, font=MONO_FONT, font_size=24, t2c={"3": COLOR_OUTPUT})


class TensorMatmul(Scene):
    def construct(self):
        title = ko("A의 행과 B의 열을 곱해 더하면 결과 한 칸이 돼요", size=30).to_edge(UP)
        self.play(Write(title))

        empty = lambda r, c: [[""] * c for _ in range(r)]
        a = grid(empty(4, 3), COLOR_INPUT, SIZE)
        b = grid(empty(3, 2), COLOR_WEIGHT, SIZE)
        c = grid(empty(4, 2), COLOR_OUTPUT, SIZE)
        for cl in c.family_members_with_points():
            cl.set_fill(opacity=0)
        # 결과 C의 행은 A의 행과, 열은 B의 열과 나란히 놓습니다.
        c.shift(RIGHT * 1.5 + DOWN * 0.9)
        a.next_to(c, LEFT, buff=0.8)
        b.next_to(c, UP, buff=0.5)
        a_label = shape_label("A (4, 3)").next_to(a, DOWN, buff=0.3)
        b_label = shape_label("B (3, 2)").next_to(b, RIGHT, buff=0.3)
        c_label = code("C = A @ B  (4, 2)", size=24, color=COLOR_OUTPUT).next_to(c, RIGHT, buff=0.3)
        self.play(FadeIn(a), FadeIn(b), FadeIn(a_label), FadeIn(b_label))
        self.play(FadeIn(c), FadeIn(c_label))

        for step, (i, j) in enumerate([(0, 0), (0, 1), (1, 0)]):
            run = 1 if step == 0 else 0.6
            self.play(
                *[highlight(a[i][k], COLOR_INPUT) for k in range(3)],
                *[highlight(b[k][j], COLOR_WEIGHT) for k in range(3)],
                run_time=run,
            )
            self.play(highlight(c[i][j], COLOR_OUTPUT), run_time=run)
            self.play(
                *[highlight(a[i][k], COLOR_INPUT, opacity=0.25) for k in range(3)],
                *[highlight(b[k][j], COLOR_WEIGHT, opacity=0.25) for k in range(3)],
                run_time=0.3,
            )
            if step == 0:
                note = ko("행과 열의 길이가 둘 다 3이라서 짝을 맞춰 곱할 수 있어요", size=24, color=COLOR_OUTPUT)
                note.to_edge(DOWN, buff=0.3)
                self.play(FadeIn(note))

        rest = [c[i][j] for i in range(4) for j in range(2) if (i, j) not in [(0, 0), (0, 1), (1, 0)]]
        self.play(LaggedStart(*[highlight(x, COLOR_OUTPUT) for x in rest], lag_ratio=0.2), run_time=1.5)
        summary = code("(4, 3) @ (3, 2) → (4, 2)", size=28, color=COLOR_OUTPUT).move_to(note)
        self.play(note.animate.become(summary))
        self.wait(1.5)
