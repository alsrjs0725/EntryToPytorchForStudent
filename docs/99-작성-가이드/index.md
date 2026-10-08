# 작성 가이드

이 사이트는 [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)로 만들어집니다. `docs/` 아래 마크다운 파일을 수정하고 `main`에 푸시하면 GitHub Pages에 자동 배포됩니다.

## 로컬에서 미리보기

```bash
pip install -r requirements-docs.txt
mkdocs serve   # http://127.0.0.1:8000
```

## 새 페이지 추가

`docs/<카테고리 번호>-<카테고리>/<문서 번호>-<제목>.md` 형식으로 파일을 만들면 사이드바 목차에 번호 순으로 자동 추가됩니다. 페이지 제목은 파일 첫 줄의 `# 제목`을 따릅니다.

## Colab 노트북 링크

실습 노트북은 `notebooks/<카테고리 번호>-<카테고리>/<문서 번호>-<제목>.ipynb`에 두고, 문서 첫머리에 Colab 링크를 붙입니다. `blob/main/` 뒤에 저장소 기준 경로를 적으면 됩니다.

```markdown
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alsrjs0725/EntryToPytorchForStudent/blob/main/notebooks/00-시작하기/01-colab-사용법.ipynb)
```

## 이미지

이미지는 `docs/images/`에 넣고 문서 위치 기준 상대 경로로 참조합니다.

```markdown
![설명](../images/example.png){ width="500" }
```

## 영상

webm·mp4 영상은 `docs/videos/`에 넣고 HTML `<video>` 태그로 넣습니다. 학습 과정 애니메이션처럼 짧은 영상은 `autoplay loop muted`를 붙이면 GIF처럼 반복 재생됩니다.

```html
<video src="../../videos/example.webm" controls autoplay loop muted playsinline width="600"></video>
```

시각화 영상은 Manim으로 만듭니다. 원본은 `animations/<카테고리>/<장면>.py`, 렌더링 결과는 `docs/videos/<카테고리>/<장면>.mp4`에 둡니다. 렌더링 방법은 [animations/README.md](https://github.com/alsrjs0725/EntryToPytorchForStudent/blob/main/animations/README.md)를 참고하세요.

!!! tip "용량"
    GitHub는 100MB가 넘는 파일을 받지 않습니다. 영상은 수 MB 이내로 줄이고, 긴 영상은 YouTube에 올려 `<iframe>`으로 넣습니다.

## 코드블럭

언어, 제목, 줄 번호, 강조 줄을 지정할 수 있고 복사 버튼이 자동으로 붙습니다.

````markdown
```python title="model.py" linenums="1" hl_lines="3"
import torch

x = torch.randn(2, 3)
print(x.shape)
```
````

결과:

```python title="model.py" linenums="1" hl_lines="3"
import torch

x = torch.randn(2, 3)
print(x.shape)
```

## 강조 박스

```markdown
!!! tip "팁"
    내용은 4칸 들여쓰기합니다.
```

!!! tip "팁"
    내용은 4칸 들여쓰기합니다.

## 수식

```markdown
$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$
```

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$
