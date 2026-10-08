"""어텐션이 다른 토큰의 값을 가중 평균해 새 벡터를 만드는 모습을 보여줍니다."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import (
    DOWN,
    UP,
    Arrow,
    FadeIn,
    FadeOut,
    GrowArrow,
    Rectangle,
    Scene,
    TransformFromCopy,
    VGroup,
    Write,
)

from common.style import COLOR_INPUT, COLOR_MUTED, COLOR_OUTPUT, COLOR_WEIGHT, ko

TOKENS = ["바다", "에", "배", "가", "떠", "있다"]
QUERY = 2  # "배"
# 설명용 예시 가중치입니다. 합이 1이 되도록 정했어요.
WEIGHTS = [0.45, 0.05, 0.2, 0.05, 0.15, 0.1]


class AttentionMix(Scene):
    def construct(self):
        title = ko("어텐션은 다른 토큰을 섞어 문맥을 담아요", size=32).to_edge(UP)
        self.play(Write(title))

        boxes = VGroup()
        for tok in TOKENS:
            box = Rectangle(width=1.5, height=0.8, color=COLOR_INPUT)
            box.add(ko(tok, size=28).move_to(box))
            boxes.add(box)
        boxes.arrange(buff=0.25).shift(UP * 1.2)
        self.play(FadeIn(boxes))

        q_box = boxes[QUERY]
        q_label = ko("쿼리: '배'는 어떤 뜻일까?", size=24, color=COLOR_WEIGHT).next_to(boxes, DOWN, buff=0.4)
        self.play(q_box.animate.set_stroke(color=COLOR_WEIGHT, width=6, family=False), FadeIn(q_label))

        target = Rectangle(width=2.2, height=0.9, color=COLOR_OUTPUT).shift(DOWN * 2.3)
        target_label = ko("새 '배' 벡터", size=26, color=COLOR_OUTPUT).move_to(target)

        arrows, weights = VGroup(), VGroup()
        for box, w in zip(boxes, WEIGHTS):
            arrow = Arrow(
                box.get_bottom(),
                target.get_top(),
                buff=0.1,
                stroke_width=2 + 22 * w,
                max_tip_length_to_length_ratio=0.08,
                color=COLOR_WEIGHT,
            ).set_opacity(0.25 + 0.75 * w / max(WEIGHTS))
            arrows.add(arrow)
            weights.add(ko(f"{w:.2f}", size=20, color=COLOR_WEIGHT).next_to(box, UP, buff=0.1))
        self.play(FadeOut(q_label))
        self.play(FadeIn(weights), *[GrowArrow(a) for a in arrows], run_time=2)
        self.play(FadeIn(target), TransformFromCopy(boxes, target_label), run_time=1.5)

        note = ko("'바다'를 많이 보고 '배'를 바다의 배로 해석해요", size=24, color=COLOR_MUTED)
        note.next_to(target, DOWN, buff=0.3)
        self.play(FadeIn(note))
        self.wait(1.5)
