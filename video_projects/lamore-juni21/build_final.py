"""Build the Lamore juni#21 edit (origin story: farm to bottle, 48s).

Same overlay architecture as juni20: raw narration audio plays continuously
and uncut, B-roll composited as opaque overlays on the raw base (PTS-shifted
so each overlay's frame 0 lands at its window start).

Two segments intentionally stay A-roll (no footage exists yet):
  - 12.88-16.48 "csemetekorától végigkövetjük a fejlődésüket" (seedling contrast)
  - 38.94-44.32 "tizenhárom éve... egészségét és egyensúlyát" (family/trust)
Per user instruction, "hidegen préseljük" and "csak és kizárólag" also stay
A-roll (pulled back from the earlier draft plan that used B-roll there).

No captions (matching the juni20 v3 preference). Music + light SFX layer to
keep house style consistent across the series.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

FFMPEG = r"C:\Users\User\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe"
FFPROBE = r"C:\Users\User\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin\ffprobe.exe"

PROJECT = Path(r"E:\CLAUDE VIDEO EDIT\Hyperframe edit\video_projects\lamore-juni21")
BROLL_DIR = Path(r"E:\CLAUDE VIDEO EDIT\videó anyagok")
STOCK_DIR = BROLL_DIR / "stock_candidates"
SFX_BUNDLED = Path(r"E:\CLAUDE VIDEO EDIT\Hyperframe edit\.agents\skills\media-use\audio\assets\sfx")
SFX_DL = Path(r"E:\CLAUDE VIDEO EDIT\Hyperframe edit\video_projects\lamore-juni20\sfx_downloaded")
MUSIC = Path(r"E:\CLAUDE VIDEO EDIT\Hyperframe edit\video_projects\lamore-juni20\music_candidates\close_up_michael_ramir_c.mp3")

RAW = PROJECT / "raw.mp4"
TRANSCRIPT = PROJECT / "edit" / "transcripts" / "raw.json"
EDIT_DIR = PROJECT / "edit"
WORK = EDIT_DIR / "overlays"
WORK.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920
GRADE = "eq=contrast=1.06:brightness=0.0:saturation=1.0,curves=master='0/0 0.25/0.23 0.75/0.77 1/1'"

SOURCES = {
    "ultetveny": BROLL_DIR / "ültetvény.mp4",
    "szuret": BROLL_DIR / "szüret.mp4",
    "asztalon": BROLL_DIR / "Lamore video - termekek az asztalon.mp4",
    "lamore_termekek": BROLL_DIR / "Lamore termékek.mp4",
    "tiszta_le": STOCK_DIR / "tiszta_le_ontese.mp4",
    "bokor_egbolt": STOCK_DIR / "homoktovis_bokor_egbolt.mp4",
    "dora_velo": BROLL_DIR / "Dora issza a velot.mp4",
}

# (source_key, offset_in_source, output_start, output_end, transition)
BEATS = [
    ("ultetveny",       0.00,  0.00,  0.64, "flash"),   # "A földtől" -- full B-roll from t=0
    ("asztalon",        0.00,  0.66,  1.38, "flash"),   # "az asztalodig"
    ("ultetveny",       0.00,  4.48,  9.02, "cross"),   # location + organic farming + irrigation
    ("bokor_egbolt",    0.50, 10.38, 12.66, "cut"),      # "figyelmet fordítunk ültetvényeinkre" -- new clip, not a 3rd ültetvény repeat
    ("szuret",          0.00, 16.64, 22.02, "cross"),   # harvest
    ("tiszta_le",       0.00, 28.12, 31.50, "cross"),   # "nincs benne semmi hozzáadott"
    ("lamore_termekek", 0.00, 35.34, 38.88, "flash"),   # "bepalackozott termékek"
    ("dora_velo",       0.00, 46.38, 48.02, "flash"),   # closing -- Dóra issza a velőt
]

# A-roll stays: 9.02-10.38, 12.88-16.48 (seedling gap), 22.24-28.08
# ("hidegen préseljük"), 31.52-35.26 ("csak és kizárólag"), 38.94-44.32
# (family/trust gap), 44.38-46.32 (CTA question).

SFX_CUES = [
    (SFX_BUNDLED / "whoosh-short.mp3",   0.02, 0.45),
    (SFX_BUNDLED / "whoosh-short.mp3",   0.62, 0.40),
    (SFX_DL / "cinematic_whoosh_fast_transition.mp3", 4.40, 0.45),
    (SFX_BUNDLED / "riser.mp3",         15.50, 0.30),
    (SFX_DL / "positive_notification.mp3", 35.30, 0.50),
    # no sfx on the closing beat, per instruction
]

CROSS_FADE_S = 0.15
FLASH_DUR_S = 0.08


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr[-4000:])
        result.check_returncode()


def probe_wh(path: Path) -> tuple[int, int]:
    out = subprocess.run(
        [FFPROBE, "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    )
    parts = [p for p in out.stdout.strip().split(",") if p]
    return int(parts[0]), int(parts[1])


def crop_to_fill_filter(path: Path) -> str:
    sw, sh = probe_wh(path)
    target_ar = W / H
    src_ar = sw / sh
    if src_ar > target_ar:
        new_w = int(sh * target_ar)
        new_w -= new_w % 2
        crop = f"crop={new_w}:{sh}:({sw}-{new_w})/2:0"
    else:
        new_h = int(sw / target_ar)
        new_h -= new_h % 2
        crop = f"crop={sw}:{new_h}:0:({sh}-{new_h})/2"
    return f"{crop},scale={W}:{H}"


def extract_overlay(idx: int, key: str, offset: float, duration: float, transition: str) -> Path:
    src = SOURCES[key]
    out_path = WORK / f"ov_{idx:02d}_{key}.mov"
    vf = f"{crop_to_fill_filter(src)},{GRADE}"
    if transition == "cross":
        vf += (
            f",format=yuva444p10le,"
            f"fade=t=in:st=0:d={CROSS_FADE_S}:alpha=1,"
            f"fade=t=out:st={max(0.0, duration - CROSS_FADE_S):.3f}:d={CROSS_FADE_S}:alpha=1"
        )
    else:
        vf += ",format=yuva444p10le"
    cmd = [
        FFMPEG, "-y",
        "-ss", f"{offset:.3f}", "-i", str(src),
        "-t", f"{duration:.3f}",
        "-vf", vf,
        "-an",
        "-c:v", "prores_ks", "-profile:v", "4444", "-qscale:v", "9",
        str(out_path),
    ]
    print(f"  [{idx:02d}] {key:16s} off={offset:5.2f} dur={duration:5.2f} ({transition})")
    run(cmd)
    return out_path


def make_flash_clip() -> Path:
    out_path = WORK / "flash.mov"
    cmd = [
        FFMPEG, "-y",
        "-f", "lavfi", "-i", f"color=white:size={W}x{H}:duration={FLASH_DUR_S}:rate=30",
        "-vf", f"format=yuva444p10le,fade=t=out:st=0:d={FLASH_DUR_S}:alpha=1",
        "-c:v", "prores_ks", "-profile:v", "4444", "-qscale:v", "9",
        str(out_path),
    ]
    run(cmd)
    return out_path


def build_video(overlay_paths: list[Path], flash_path: Path) -> Path:
    inputs: list[str] = ["-i", str(RAW)]
    for p in overlay_paths:
        inputs += ["-i", str(p)]
    flash_input_index = len(overlay_paths) + 1
    inputs += ["-i", str(flash_path)]

    filter_parts: list[str] = [f"[0:v]{GRADE}[graded]"]
    current = "[graded]"

    for i, (key, offset, out_start, out_end, transition) in enumerate(BEATS):
        src_idx = i + 1
        shifted = f"[ov{i}]"
        filter_parts.append(f"[{src_idx}:v]setpts=PTS-STARTPTS+{out_start:.3f}/TB{shifted}")
        nxt = f"[v{i}]"
        filter_parts.append(
            f"{current}{shifted}overlay=eof_action=pass:"
            f"enable='between(t,{out_start:.3f},{out_end:.3f})'{nxt}"
        )
        current = nxt

    flash_beats = [i for i, b in enumerate(BEATS) if b[4] == "flash"]
    for j, i in enumerate(flash_beats):
        _key, _offset, out_start, _out_end, _transition = BEATS[i]
        flash_start = max(0.0, out_start - FLASH_DUR_S / 2)
        flash_end = flash_start + FLASH_DUR_S
        shifted = f"[fl{j}]"
        filter_parts.append(f"[{flash_input_index}:v]setpts=PTS-STARTPTS+{flash_start:.3f}/TB{shifted}")
        nxt = f"[f{j}]"
        filter_parts.append(
            f"{current}{shifted}overlay=eof_action=pass:"
            f"enable='between(t,{flash_start:.3f},{flash_end:.3f})'{nxt}"
        )
        current = nxt

    filter_parts.append(f"{current}null[outv]")
    filter_complex = ";".join(filter_parts)
    video_out = EDIT_DIR / "video_only.mp4"
    cmd = [
        FFMPEG, "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-an",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        str(video_out),
    ]
    print("compositing video (overlays + grade, no captions)...")
    run(cmd)
    return video_out


def build_audio(total_duration: float) -> Path:
    inputs: list[str] = ["-i", str(RAW)]
    inputs += ["-i", str(MUSIC)]
    for f, _t, _v in SFX_CUES:
        inputs += ["-i", str(f)]

    filter_parts: list[str] = []
    fade_start = max(0.0, total_duration - 1.5)
    filter_parts.append(
        f"[1:a]atrim=0:{total_duration:.3f},volume=0.18,"
        f"afade=t=out:st={fade_start:.3f}:d=1.5[music_raw]"
    )
    filter_parts.append(
        "[music_raw][0:a]sidechaincompress=threshold=0.04:ratio=10:attack=15:release=400[music_duck]"
    )

    sfx_labels: list[str] = []
    for i, (_f, t, vol) in enumerate(SFX_CUES):
        src_idx = i + 2
        lbl = f"sfx{i}"
        delay_ms = int(t * 1000)
        filter_parts.append(
            f"[{src_idx}:a]volume={vol},adelay={delay_ms}|{delay_ms},apad[{lbl}]"
        )
        sfx_labels.append(f"[{lbl}]")

    mix_inputs = "[0:a][music_duck]" + "".join(sfx_labels)
    n_mix = 2 + len(sfx_labels)
    filter_parts.append(
        f"{mix_inputs}amix=inputs={n_mix}:duration=first:normalize=0[aout]"
    )

    filter_complex = ";".join(filter_parts)
    audio_out = EDIT_DIR / "audio_mix.m4a"
    cmd = [
        FFMPEG, "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[aout]",
        "-t", f"{total_duration:.3f}",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        str(audio_out),
    ]
    print("mixing audio (narration + ducked music + sfx)...")
    run(cmd)
    return audio_out


def main() -> None:
    data = json.loads(TRANSCRIPT.read_text(encoding="utf-8"))
    total_duration = max(w["end"] for w in data["words"] if w.get("type") == "word") + 0.7

    print(f"extracting {len(BEATS)} b-roll overlay beats...")
    overlay_paths = [
        extract_overlay(i, key, offset, out_end - out_start, transition)
        for i, (key, offset, out_start, out_end, transition) in enumerate(BEATS)
    ]
    flash_path = make_flash_clip()

    video_only = build_video(overlay_paths, flash_path)
    audio_mix = build_audio(total_duration)

    muxed = EDIT_DIR / "muxed.mp4"
    run([
        FFMPEG, "-y",
        "-i", str(video_only), "-i", str(audio_mix),
        "-map", "0:v", "-map", "1:a",
        "-c:v", "copy", "-c:a", "copy",
        "-movflags", "+faststart",
        str(muxed),
    ])

    final_out = EDIT_DIR / "final.mp4"
    run([
        FFMPEG, "-y", "-i", str(muxed),
        "-c:v", "copy",
        "-af", "loudnorm=I=-14:TP=-1:LRA=11",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        str(final_out),
    ])

    size_mb = final_out.stat().st_size / (1024 * 1024)
    print(f"\ndone: {final_out} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
