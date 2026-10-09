"""모든 장면이 함께 쓰는 색, 글꼴, 도우미 함수."""

from manim import BLUE, GREEN, GREY_B, ORANGE, RED, TEAL, WHITE, YELLOW, Text

# 한글 글꼴. Colab과 우분투에서는 fonts-noto-cjk 패키지로 설치됩니다.
FONT = "Noto Sans CJK KR"

# 같은 개념은 모든 영상에서 같은 색으로 보여줍니다.
COLOR_INPUT = BLUE  # 입력 x
COLOR_WEIGHT = ORANGE  # 가중치 W
COLOR_BIAS = TEAL  # 편향 b
COLOR_OUTPUT = YELLOW  # 출력 y
COLOR_LOSS = RED  # 손실
COLOR_GRAD = GREEN  # 손실이 줄어드는 방향 (기울기 화살표)
COLOR_TEXT = WHITE
COLOR_MUTED = GREY_B


def ko(text: str, size: int = 36, color=COLOR_TEXT, **kwargs) -> Text:
    """한글이 깨지지 않도록 글꼴을 지정한 Text를 만듭니다.

    격자 위에서도 읽히도록 반투명 배경을 깔고 항상 맨 앞에 그립니다.
    """
    label = Text(text, font=FONT, font_size=size, color=color, **kwargs)
    label.add_background_rectangle(opacity=0.8, buff=0.1)
    label.set_z_index(1)
    return label
