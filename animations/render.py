"""Manim 장면을 렌더링하고 결과 영상을 docs/videos/로 복사합니다.

사용법 (저장소 루트에서):
    python animations/render.py animations/01-레이어-이론/linear_layer.py LinearLayer
    python animations/render.py animations/01-레이어-이론/linear_layer.py LinearLayer --quality h

결과: docs/videos/01-레이어-이론/linear_layer.mp4
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEDIA_DIR = ROOT / "animations" / "media"
VIDEO_DIR = ROOT / "docs" / "videos"

# l: 480p15, m: 720p30, h: 1080p60
QUALITY = {"l": "480p15", "m": "720p30", "h": "1080p60"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scene_file", type=Path)
    parser.add_argument("scene_name")
    parser.add_argument("--quality", choices=QUALITY, default="m")
    args = parser.parse_args()

    scene_file = args.scene_file.resolve()
    subprocess.run(
        [
            sys.executable, "-m", "manim", "render",
            f"-q{args.quality}",
            "--media_dir", str(MEDIA_DIR),
            str(scene_file), args.scene_name,
        ],
        check=True,
    )

    rendered = MEDIA_DIR / "videos" / scene_file.stem / QUALITY[args.quality] / f"{args.scene_name}.mp4"
    target = VIDEO_DIR / scene_file.parent.name / f"{scene_file.stem}.mp4"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(rendered, target)
    size_mb = target.stat().st_size / 1_000_000
    print(f"복사함: {target.relative_to(ROOT)} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
