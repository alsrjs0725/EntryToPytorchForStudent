# 애니메이션 (Manim)

3Blue1Brown 영상에 쓰인 [Manim](https://www.manim.community/)으로 개념 영상을 만듭니다. 이 저장소는 커뮤니티 버전(Manim Community, `manim` 패키지)을 씁니다.

## 폴더 구조

```
animations/
├── common/style.py           # 공통 색, 한글 글꼴, ko() 도우미
├── 01-레이어-이론/            # 커리큘럼 카테고리와 같은 이름
│   └── linear_layer.py       # 장면 파일 (예시)
├── render.py                 # 렌더링 후 docs/videos/로 복사
├── setup.sh                  # 우분투용 설치 스크립트
└── colab_render.ipynb        # Colab에서 렌더링하는 노트북
```

렌더링 결과는 `docs/videos/<카테고리>/<장면 파일 이름>.mp4`에 저장됩니다.

## Colab에서 렌더링

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alsrjs0725/EntryToPytorchForStudent/blob/main/animations/colab_render.ipynb)

노트북을 열고 셀을 순서대로 실행하면 영상을 미리 보고 내려받을 수 있어요.

## 로컬이나 클라우드 에이전트에서 렌더링

```bash
bash animations/setup.sh   # 우분투 기준. 시스템 패키지 설치와 .venv 생성

.venv/bin/python animations/render.py animations/01-레이어-이론/linear_layer.py LinearLayer
```

- `--quality l`(480p)로 빠르게 확인하고, 커밋할 때는 기본값 `m`(720p)을 씁니다.
- 수식(`MathTex`)을 쓰려면 LaTeX(`texlive`, `texlive-latex-extra`, `dvisvgm`)가 추가로 필요합니다. 수식이 꼭 필요하지 않으면 `ko()` 텍스트로 대신합니다.

## 문서에 넣기

```html
<video src="../../videos/01-레이어-이론/linear_layer.mp4" controls autoplay loop muted playsinline width="600"></video>
```
