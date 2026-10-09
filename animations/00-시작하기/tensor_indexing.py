"""인덱싱으로 (3, 4) 텐서에서 원하는 칸을 꺼내는 모습을 보여줍니다."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import DOWN, LEFT, RIGHT, UP, FadeIn, FadeOut, Scene, Transform, VGroup, Write

from common.style import COLOR_INPUT, COLOR_MUTED, COLOR_OUTPUT, ko
from common.tensor import cell, code, grid, highlight

# m = torch.arange(12).reshape(3, 4)
M = [[4 * i + j for j in range(4)] for i in range(3)]

# (코드, 꺼내는 칸의 (행, 열) 목록, 결과를 그릴 (행 수, 열 수), 결과 모양)
STEPS = [
    ("m[0]", [(0, j) for j in range(4)], (1, 4), "(4,)"),
    ("m[:, 1]", [(i, 1) for i in range(3)], (1, 3), "(3,)"),
    ("m[1:, 2:]", [(1, 2), (1, 3), (2, 2), (2, 3)], (2, 2), "(2, 2)"),
    ("m[m > 6]", [(i, j) for i in range(3) for j in range(4) if M[i][j] > 6], (1, 5), "(5,)"),
]


class TensorIndexing(Scene):
    def construct(self):
        title = ko("인덱싱은 원하는 칸만 꺼내요", size=32).to_edge(UP)
        self.play(Write(title))

        m = grid(M).shift(LEFT * 3 + UP * 0.2)
        # 행 번호와 열 번호
        row_ids = VGroup(*[code(str(i), size=22, color=COLOR_MUTED).next_to(m[i], LEFT, buff=0.2) for i in range(3)])
        col_ids = VGroup(*[code(str(j), size=22, color=COLOR_MUTED).next_to(m[0][j], UP, buff=0.15) for j in range(4)])
        name = code("m  # (3, 4)", size=24).next_to(m, DOWN, buff=0.3)
        self.play(FadeIn(m), FadeIn(row_ids), FadeIn(col_ids), FadeIn(name))

        label = code(STEPS[0][0]).to_edge(DOWN, buff=0.6)
        self.play(Write(label))
        for i, (text, picked, (rows, cols), shape) in enumerate(STEPS):
            if i > 0:
                self.play(Transform(label, code(text).move_to(label)))
            self.play(*[highlight(m[r][c], COLOR_OUTPUT) for r, c in picked], run_time=0.8)

            result = VGroup(*[cell(M[r][c], COLOR_OUTPUT) for r, c in picked])
            result.arrange_in_grid(rows=rows, cols=cols, buff=0).move_to(RIGHT * 3.2 + UP * 0.2)
            copies = VGroup(*[m[r][c].copy() for r, c in picked])
            shape_text = code(shape, size=26, color=COLOR_OUTPUT).next_to(result, DOWN, buff=0.3)
            self.play(Transform(copies, result), run_time=1.2)
            self.play(FadeIn(shape_text))
            self.wait(1)
            self.play(
                FadeOut(copies),
                FadeOut(shape_text),
                *[highlight(m[r][c], COLOR_INPUT, opacity=0.25) for r, c in picked],
                run_time=0.6,
            )
        self.wait(0.5)
