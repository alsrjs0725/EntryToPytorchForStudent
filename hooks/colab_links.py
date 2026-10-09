"""Colab 링크를 새 탭에서 열리게 합니다.

문서마다 `{target=_blank}`를 붙이지 않아도, 빌드할 때 Colab으로 가는 모든 링크에
`target="_blank"`와 `rel="noopener"`를 넣습니다.
"""

import re

COLAB_LINK = re.compile(r'<a href="https://colab\.research\.google\.com/')


def on_page_content(html, **kwargs):
    return COLAB_LINK.sub(
        '<a target="_blank" rel="noopener" href="https://colab.research.google.com/',
        html,
    )
