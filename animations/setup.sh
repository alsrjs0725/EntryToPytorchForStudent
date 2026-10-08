#!/usr/bin/env bash
# 우분투(로컬, 클라우드 에이전트)에서 Manim 렌더링 환경을 준비합니다.
# 사용법: bash animations/setup.sh   → 이후 .venv/bin/python animations/render.py ...
set -euo pipefail
cd "$(dirname "$0")/.."

SUDO=""
[ "$(id -u)" -ne 0 ] && SUDO="sudo"
$SUDO apt-get update -qq
$SUDO apt-get install -y -qq libpango1.0-dev pkg-config fonts-noto-cjk ffmpeg > /dev/null

[ -d .venv ] || python3 -m venv .venv
.venv/bin/pip install -q -r animations/requirements.txt
.venv/bin/python -c "import manim; print('manim', manim.__version__)"
