"""m[m > 6]이 참/거짓 마스크를 만든 뒤 True인 칸만 걸러내는 두 단계임을 보여줍니다."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import DOWN, LEFT, RIGHT, UP, Arrow, FadeIn, FadeOut, ReplacementTransform, Scene, Text, Transform, VGroup, Write

from common.style import COLOR_INPUT, COLOR_MUTED, COLOR_OUTPUT, FONT, ko
from common.tensor import cell, code, grid, highlight

# m = torch.arange(12).reshape(3, 4)
M = [[4 * i + j for j in range(4)] for i in range(3)]
SIZE = 0.8


def mask_cell(flag: bool) -> VGroup:
    color = COLOR_OUTPUT if flag else COLOR_MUTED
    c = cell("", color, SIZE)
    c[0].set_fill(color, opacity=0.6 if flag else 0.15)
    label = Text(str(flag), font=FONT, font_size=18, color=color if not flag else "#000000").move_to(c[0])
    c.remove(c[1])
    c.add(label)
    return c


class TensorMask(Scene):
    def construct(self):
        title = ko("m > 6은 칸마다 참/거짓을 검사해요", size=32).to_edge(UP)
        self.play(Write(title))

        m = grid(M, COLOR_INPUT, SIZE).move_to(LEFT * 3.4 + UP * 0.8)
        m_label = code("m  # (3, 4)", size=22).next_to(m, DOWN, buff=0.25)
        self.play(FadeIn(m), FadeIn(m_label))

        # 1단계: 같은 모양의 참/거짓 텐서(마스크)를 만듭니다.
        label = code("mask = m > 6").to_edge(DOWN, buff=0.5)
        self.play(Write(label))
        mask = VGroup(
            *[VGroup(*[mask_cell(v > 6) for v in row]).arrange(RIGHT, buff=0) for row in M]
        ).arrange(DOWN, buff=0).move_to(RIGHT * 3.4 + UP * 0.8)
        arrow = Arrow(m.get_right(), mask.get_left(), buff=0.3, color=COLOR_MUTED)
        arrow_label = code("> 6", size=24, color=COLOR_MUTED).next_to(arrow, UP, buff=0.1)
        self.play(FadeIn(arrow), FadeIn(arrow_label))
        copies = VGroup(*[m[i][j].copy() for i in range(3) for j in range(4)])
        targets = VGroup(*[mask[i][j] for i in range(3) for j in range(4)])
        self.play(ReplacementTransform(copies, targets), run_time=1.5)
        mask_label = code("mask  # (3, 4)", size=22, color=COLOR_OUTPUT).next_to(mask, DOWN, buff=0.25)
        note = ko("인덱스가 아니라 m과 모양이 같은 참/거짓 텐서예요", size=24, color=COLOR_OUTPUT)
        note.next_to(label, UP, buff=0.3)
        self.play(FadeIn(mask_label), FadeIn(note))
        self.wait(1.5)

        # 2단계: 마스크를 겹쳐 True인 칸의 값만 꺼냅니다.
        new_title = ko("m[mask]는 True인 칸의 값만 꺼내요", size=32).move_to(title)
        self.play(
            Transform(title, new_title),
            Transform(label, code("m[mask]   # m[m > 6]과 같아요").move_to(label)),
            FadeOut(note),
        )
        picked = [(i, j) for i in range(3) for j in range(4) if M[i][j] > 6]
        self.play(
            *[highlight(m[i][j], COLOR_OUTPUT) for i, j in picked],
            *[mask[i][j].animate.set_opacity(0.3) for i in range(3) for j in range(4) if (i, j) not in picked],
            run_time=1,
        )
        result = VGroup(*[cell(M[i][j], COLOR_OUTPUT, SIZE) for i, j in picked]).arrange(RIGHT, buff=0)
        result.move_to(DOWN * 1.6)
        shape_text = code("(5,)", size=24, color=COLOR_OUTPUT).next_to(result, RIGHT, buff=0.3)
        self.play(ReplacementTransform(VGroup(*[m[i][j].copy() for i, j in picked]), result), run_time=1.5)
        self.play(FadeIn(shape_text))
        self.wait(1.5)
