"""텐서를 칸 격자로 그리는 도우미 함수."""

from manim import DOWN, RIGHT, Square, Text, VGroup

from .style import COLOR_INPUT, COLOR_TEXT, FONT

# 코드 글꼴. fonts-noto-cjk에 함께 들어 있어서 한글 주석도 깨지지 않습니다.
MONO_FONT = "Noto Sans Mono CJK KR"
CELL_SIZE = 0.7


def code(text: str, size: int = 28, color=COLOR_TEXT, **kwargs) -> Text:
    """코드 한 줄을 고정폭 글꼴로 만듭니다."""
    label = Text(text, font=MONO_FONT, font_size=size, color=color, **kwargs)
    label.set_z_index(1)
    return label


def cell(value="", color=COLOR_INPUT, size: float = CELL_SIZE) -> VGroup:
    """값 하나를 담은 칸. [0]은 네모, [1]은 숫자입니다."""
    box = Square(side_length=size, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.25)
    number = Text(str(value), font=FONT, font_size=int(size * 34), color=COLOR_TEXT).move_to(box)
    return VGroup(box, number)


def grid(rows, color=COLOR_INPUT, size: float = CELL_SIZE) -> VGroup:
    """2차원 리스트를 격자로 만듭니다. g[i][j]가 i행 j열 칸입니다."""
    return VGroup(
        *[VGroup(*[cell(v, color, size) for v in row]).arrange(RIGHT, buff=0) for row in rows]
    ).arrange(DOWN, buff=0)


def highlight(c: VGroup, color, opacity: float = 0.7) -> VGroup:
    """칸의 색을 바꾸는 애니메이션 대상(.animate)을 돌려줍니다."""
    return c[0].animate.set_fill(color, opacity=opacity).set_stroke(color)
