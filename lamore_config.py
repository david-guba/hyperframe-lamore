"""Shared, portable path configuration for the Lamore build scripts.

Every build_final*.py imports this instead of hardcoding absolute paths.
All the "external" asset locations (B-roll library, bundled SFX, shared
music/SFX pulled from the juni20 project) can be overridden with
environment variables -- set them in a `.env` file (see `.env.example`)
or export them directly. If unset, they fall back to sensible defaults:
first a repo-relative `assets/` layout (for cloud/portable use), then the
original local Windows paths this project was developed on.

To run this on a new machine (cloud VM, another PC):
  1. Download the B-roll/stock library from Drive to `assets/broll/`
     (relative to the repo root), or set LAMORE_BROLL_DIR to wherever
     you put it.
  2. Make sure ffmpeg/ffprobe are on PATH (or set FFMPEG_BIN/FFPROBE_BIN).
  3. The bundled SFX pack (whoosh/riser/pop/etc.) ships with the
     Hyperframes skill install; point LAMORE_SFX_BUNDLED_DIR at it, or
     copy those files into `assets/sfx_bundled/`.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent


def _env_path(var: str, *fallbacks: Path) -> Path:
    """Resolve a path from an env var, or the first existing fallback,
    or the first fallback if none exist (so a clear "not found" error
    surfaces later instead of here)."""
    value = os.environ.get(var)
    if value:
        return Path(value)
    for fb in fallbacks:
        if fb.exists():
            return fb
    return fallbacks[0]


def _env_bin(var: str, default_name: str, *fallback_paths: Path) -> str:
    """Resolve a tool binary: env var > bare name if it's on PATH >
    first existing fallback absolute path > bare name (last resort,
    will error clearly at call time if truly missing)."""
    value = os.environ.get(var)
    if value:
        return value
    if shutil.which(default_name):
        return default_name
    for fb in fallback_paths:
        if fb.exists():
            return str(fb)
    return default_name


# -------- Tools ---------------------------------------------------------

FFMPEG = _env_bin(
    "FFMPEG_BIN", "ffmpeg",
    Path(r"C:\Users\User\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe"),
)
FFPROBE = _env_bin(
    "FFPROBE_BIN", "ffprobe",
    Path(r"C:\Users\User\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin\ffprobe.exe"),
)

# -------- Shared asset directories --------------------------------------

# The B-roll / stock-footage library (shared across all three videos).
BROLL_DIR = _env_path(
    "LAMORE_BROLL_DIR",
    REPO_ROOT / "assets" / "broll",
    Path(r"E:\CLAUDE VIDEO EDIT\videó anyagok"),
)
STOCK_DIR = BROLL_DIR / "stock_candidates"

# Bundled SFX pack that ships with the Hyperframes skill install
# (whoosh/riser/pop/impact/etc.).
SFX_BUNDLED = _env_path(
    "LAMORE_SFX_BUNDLED_DIR",
    REPO_ROOT / "assets" / "sfx_bundled",
    Path(r"E:\CLAUDE VIDEO EDIT\Hyperframe edit\.agents\skills\media-use\audio\assets\sfx"),
)

# juni17 and juni21 both reuse SFX/music that were originally downloaded
# into the juni20 project folder rather than duplicated per-project.
SHARED_PROJECT_ASSETS_DIR = _env_path(
    "LAMORE_SHARED_ASSETS_DIR",
    REPO_ROOT / "video_projects" / "lamore-juni20",
    Path(r"E:\CLAUDE VIDEO EDIT\Hyperframe edit\video_projects\lamore-juni20"),
)
SHARED_SFX_DL = SHARED_PROJECT_ASSETS_DIR / "sfx_downloaded"
SHARED_MUSIC = SHARED_PROJECT_ASSETS_DIR / "music_candidates" / "close_up_michael_ramir_c.mp3"
