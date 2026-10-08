"""Manim 장면을 렌더링하고 결과 영상을 docs/videos/로 복사합니다.

사용법 (저장소 루트에서):
    python animations/render.py animations/01-레이어-이론/linear_layer.py LinearLayer
    python animations/render.py animations/01-레이어-이론/linear_layer.py LinearLayer --quality h
    python animations/render.py --all --cache-dir ~/.cache/entry-manim   # 배포용: 모든 장면

결과: docs/videos/01-레이어-이론/linear_layer.mp4

--all은 animations/<카테고리>/*.py마다 파일 안의 Scene 클래스 하나를 렌더링합니다.
--cache-dir를 주면 장면 파일, common/, requirements.txt, 화질이 같을 때 렌더링을 건너뛰고 캐시를 씁니다.
"""

import argparse
import ast
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANIM_DIR = ROOT / "animations"
MEDIA_DIR = ANIM_DIR / "media"
VIDEO_DIR = ROOT / "docs" / "videos"

# l: 480p15, m: 720p30, h: 1080p60
QUALITY = {"l": "480p15", "m": "720p30", "h": "1080p60"}


def find_scene_files() -> list[Path]:
    # 카테고리 폴더는 "01-레이어-이론"처럼 숫자로 시작합니다. common/ 등은 제외됩니다.
    return sorted(p for p in ANIM_DIR.glob("[0-9]*/*.py") if not p.name.startswith("_"))


def find_scene_name(scene_file: Path) -> str:
    tree = ast.parse(scene_file.read_text(encoding="utf-8"))
    names = [
        node.name
        for node in tree.body
        if isinstance(node, ast.ClassDef)
        and any(getattr(base, "id", getattr(base, "attr", "")).endswith("Scene") for base in node.bases)
    ]
    if len(names) != 1:
        sys.exit(f"{scene_file.relative_to(ROOT)}: Scene 클래스가 정확히 하나여야 합니다 (찾음: {names})")
    return names[0]


def source_hash(scene_file: Path, scene_name: str, quality: str) -> str:
    h = hashlib.sha256(f"{scene_name}:{quality}".encode())
    deps = [scene_file, ANIM_DIR / "requirements.txt", *sorted((ANIM_DIR / "common").glob("*.py"))]
    for path in deps:
        h.update(path.read_bytes())
    return h.hexdigest()[:16]


def render(scene_file: Path, scene_name: str, quality: str, cache_dir: Path | None) -> None:
    target = VIDEO_DIR / scene_file.parent.name / f"{scene_file.stem}.mp4"
    target.parent.mkdir(parents=True, exist_ok=True)

    cached = None
    if cache_dir:
        cached = cache_dir / f"{scene_file.stem}-{source_hash(scene_file, scene_name, quality)}.mp4"
        if cached.exists():
            shutil.copy(cached, target)
            print(f"캐시 사용: {target.relative_to(ROOT)}")
            return

    subprocess.run(
        [
            sys.executable, "-m", "manim", "render",
            f"-q{quality}",
            "--media_dir", str(MEDIA_DIR),
            str(scene_file), scene_name,
        ],
        check=True,
    )

    rendered = MEDIA_DIR / "videos" / scene_file.stem / QUALITY[quality] / f"{scene_name}.mp4"
    shutil.copy(rendered, target)
    if cached:
        cached.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(rendered, cached)
    size_mb = target.stat().st_size / 1_000_000
    print(f"복사함: {target.relative_to(ROOT)} ({size_mb:.1f} MB)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scene_file", type=Path, nargs="?")
    parser.add_argument("scene_name", nargs="?")
    parser.add_argument("--all", action="store_true", help="animations/<카테고리>/의 모든 장면을 렌더링")
    parser.add_argument("--quality", choices=QUALITY, default="m")
    parser.add_argument("--cache-dir", type=Path, help="렌더링 결과를 재사용할 캐시 폴더")
    args = parser.parse_args()

    cache_dir = args.cache_dir.expanduser().resolve() if args.cache_dir else None

    if args.all:
        for scene_file in find_scene_files():
            render(scene_file, find_scene_name(scene_file), args.quality, cache_dir)
        return

    if not args.scene_file:
        parser.error("scene_file 또는 --all이 필요합니다")
    scene_file = args.scene_file.resolve()
    render(scene_file, args.scene_name or find_scene_name(scene_file), args.quality, cache_dir)


if __name__ == "__main__":
    main()
