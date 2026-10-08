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

## 배포 시 자동 렌더링 (홈서버)

`main`에 머지되면 [배포 워크플로](../.github/workflows/deploy-docs.yml)가 홈서버(self-hosted 러너)에서 모든 장면을 렌더링하고 사이트와 함께 GitHub Pages에 올립니다.

- 장면 파일 하나에 `Scene` 클래스 하나를 둡니다. `render.py --all`이 파일마다 그 클래스를 찾아 렌더링합니다.
- 장면 파일, `common/`, `requirements.txt`가 바뀌지 않은 장면은 서버 캐시를 써서 다시 렌더링하지 않습니다.
- 홈서버가 꺼져 있으면 배포가 대기 상태로 멈춥니다. 켜지면 이어서 진행됩니다.

### 서버에서 한 번만 할 일 (Docker)

`runner/`에 러너와 Manim 환경을 담은 Docker 이미지가 있습니다. 서버에는 Docker만 있으면 됩니다.

1. GitHub Settings → Developer settings → Fine-grained tokens에서 토큰을 만듭니다. 이 저장소만 선택하고, Repository permissions의 **Administration**을 Read and write로 줍니다.
2. 서버에서 실행합니다.

    ```bash
    git clone https://github.com/alsrjs0725/EntryToPytorchForStudent.git
    cd EntryToPytorchForStudent/runner
    cp .env.example .env   # ACCESS_TOKEN에 1번 토큰을 넣습니다
    docker compose up -d --build
    ```

3. 저장소 Settings → Actions → Runners에 `homeserver-manim`이 Idle로 보이면 됩니다. Actions 탭에서 **Deploy docs**를 수동 실행(Run workflow)해 확인합니다.

컨테이너는 켜질 때 러너를 등록하고, `docker compose down`으로 멈출 때 등록을 해제합니다. 서버가 재부팅되면 자동으로 다시 켜집니다.

> 러너가 저장소 코드를 실행하므로 워크플로에 `pull_request` 트리거를 넣지 않습니다. 포크에서 온 PR 코드가 홈서버에서 실행될 수 있습니다.

## 문서에 넣기

```html
<video src="../../videos/01-레이어-이론/linear_layer.mp4" controls autoplay loop muted playsinline width="600"></video>
```
