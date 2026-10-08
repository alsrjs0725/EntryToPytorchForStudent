# 작성 가이드

이 사이트는 [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)로 만들어집니다. `docs/` 아래 마크다운 파일을 수정하고 `main`에 푸시하면 GitHub Pages에 자동 배포됩니다.

## 로컬에서 미리보기

```bash
pip install -r requirements-docs.txt
mkdocs serve   # http://127.0.0.1:8000
```

## 새 페이지 추가

1. `docs/chapters/`에 `.md` 파일을 만듭니다.
2. `mkdocs.yml`의 `nav`에 항목을 추가합니다.

## 이미지

이미지는 `docs/images/`에 넣고 상대 경로로 참조합니다.

```markdown
![설명](../images/example.png){ width="500" }
```

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
