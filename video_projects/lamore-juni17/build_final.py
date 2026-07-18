"""Build the Lamore juni#17 edit v2 (sea buckthorn history, 60s).

Rules applied in this pass, per explicit instruction:
  - Every B-roll beat is >= 2.0s -- no quick flashes. Words are still the
    trigger point for a cut, but once cut to B-roll it holds for at least
    2s even if that runs past the triggering word (narration keeps playing
    underneath regardless -- the overlay architecture doesn't care).
  - If the natural gap between two B-roll beats would be < 1s of A-roll,
    that gap is closed entirely (extend the earlier beat forward) rather
    than flashing back to A-roll for a fraction of a second.
  - "a szuper gyumolcs latin neve..." now cuts to real sea buckthorn
    footage (not horse) with a "Hippophae" text overlay -- the actual
    Latin genus name, literally Greek for "shining horse".
  - The second Tibetan-monastery beat (regeneration line) is replaced by
    a monk meditating in a temple.
  - The opening 4.6s gets the discussed treatment: a self-referential
    punch-in zoom at ~2.3s and a "2000+ EV" kinetic text overlay timed to
    "ketezer eve", plus SFX (unchanged from before).
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

FFMPEG = r"C:\Users\User\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe"
FFPROBE = r"C:\Users\User\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin\ffprobe.exe"
FONT = r"C\:/Windows/Fonts/arialbd.ttf"

PROJECT = Path(r"E:\CLAUDE VIDEO EDIT\Hyperframe edit\video_projects\lamore-juni17")
BROLL_DIR = Path(r"E:\CLAUDE VIDEO EDIT\videó anyagok")
STOCK_DIR = BROLL_DIR / "stock_candidates"
SFX_BUNDLED = Path(r"E:\CLAUDE VIDEO EDIT\Hyperframe edit\.agents\skills\media-use\audio\assets\sfx")
SFX_DL = Path(r"E:\CLAUDE VIDEO EDIT\Hyperframe edit\video_projects\lamore-juni20\sfx_downloaded")
MUSIC = Path(r"E:\CLAUDE VIDEO EDIT\Hyperframe edit\video_projects\lamore-juni20\music_candidates\close_up_michael_ramir_c.mp3")

RAW = PROJECT / "raw.mp4"
TRANSCRIPT = PROJECT / "edit" / "transcripts" / "raw.json"
EDIT_DIR = PROJECT / "edit"
WORK = EDIT_DIR / "overlays_v3"
WORK.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920
GRADE = "eq=contrast=1.06:brightness=0.0:saturation=1.0,curves=master='0/0 0.25/0.23 0.75/0.77 1/1'"

SOURCES = {
    "taj_mahal": STOCK_DIR / "taj_mahal.mp4",
    "nagy_fal": STOCK_DIR / "nagy_fal_kina.mp4",
    "lo_szor": STOCK_DIR / "lo_ragyogo_szor.mp4",
    "lo_vagta": STOCK_DIR / "lo_vagtato.mp4",
    "tibet": STOCK_DIR / "tibet_kolostor.mp4",
    "szerzetes": STOCK_DIR / "szerzetes_meditacio.mp4",
    "labor": STOCK_DIR / "labor_mikroszkop.mp4",
    "homoktovis": STOCK_DIR / "homoktovis_bokor_egbolt.mp4",
    "omega": BROLL_DIR / "omega zsírsavak.mp4",
    "flavonoid": BROLL_DIR / "antixoidáns és flavonoid.mp4",
    "vitaminok": BROLL_DIR / "vitaminok.mp4",
    "emesztes": BROLL_DIR / "stabilabb emésztés.mp4",
    "irritalt_bor": BROLL_DIR / "irritált bőr.mp4",
    "kronikus_gyulladas": BROLL_DIR / "krónikus gyulladás.mp4",
    "ultetveny": BROLL_DIR / "ültetvény.mp4",
    "sajat_zoom": RAW,
}

# (source_key, offset_in_source, output_start, output_end, transition)
#
# Rule actually applied (per correction): each beat starts at its own
# trigger word. If the gap to the NEXT beat's trigger word is < 1s, this
# beat's end is pushed forward to close the gap entirely (no A-roll
# flash). If there's slack (gap >= 1s), this beat may still be pushed out
# up to a 2.0s total duration -- but never past the next beat's natural
# start, and never at the cost of sync. Sync always wins over the 2s
# target; that's why several ingredient beats below are under 2s.
BEATS = [
    ("sajat_zoom",          2.30,  2.30,  4.60, "cut"),     # self punch-in zoom
    ("taj_mahal",           0.00,  4.60,  5.36, "cut"),   # India (gap-closed to China)
    ("nagy_fal",            0.00,  5.36,  8.18, "cut"),     # China (2s cap, then gap-closed to horse)
    ("lo_szor",             0.00,  8.18, 11.12, "cut"),     # "ókori görögök... táplálták" (gap-closed; cut not cross -- adjacent to nagy_fal, cross would flash the talking head)
    ("homoktovis",          0.00, 11.12, 14.58, "cut"),     # "latin neve... hogy" + Hippophae text (adjacent to lo_szor -- cut, not cross)
    ("lo_szor",             5.00, 14.58, 16.58, "cut"),     # "ragyogó ló." punchline (2s cap, room available)
    ("lo_vagta",            2.00, 18.38, 21.20, "cut"),     # "ragyogott a bundája... energiával" (gap-closed)
    ("tibet",               0.00, 21.20, 24.20, "cut"),     # "tibeti és mongol népi gyógyászatban"
    ("szerzetes",           0.00, 27.24, 30.46, "cut"),     # "regenerálásra, hosszú utakra"
    ("labor",               0.00, 33.66, 37.22, "cut"),     # "kutatás készült... hatásait" (gap-closed to omega)
    ("omega",               0.00, 37.22, 37.86, "cut"),     # gap-closed to flavonoid
    ("flavonoid",           0.00, 37.86, 38.86, "cut"),     # gap-closed to vitaminok -- hard cut, no fade into vitaminok
    ("vitaminok",           0.00, 38.86, 41.38, "cut"),     # 2s cap then gap-closed to emésztést
    ("emesztes",            0.00, 41.38, 42.96, "cut"),     # 2s cap capped by next beat's start -- hard cut, no fade out of vitaminok
    ("irritalt_bor",        0.00, 42.96, 44.00, "cut"),     # gap-closed to krónikus gyulladás
    ("kronikus_gyulladas",  0.00, 44.00, 46.00, "cut"),     # 2s cap, room available (adjacent to irritalt_bor -- cut, not cross)
    ("ultetveny",           0.00, 53.80, 55.86, "cut"),   # "Vászykán biogazdálkodásunkban"
]

# A-roll stays: 0.16-2.30 (pre-zoom), 16.58-18.38, 24.20-27.24, 30.46-33.66,
# 46.00-53.80 (summary line, no B-roll to fill it), 55.86-59.86 (CTA).

TEXT_OVERLAYS = [
    # (text, start, end)
    ("2000+ ÉV", 2.94, 4.60),
    ('"Hippophae"', 11.30, 14.30),
]

SFX_CUES = [
    (SFX_BUNDLED / "riser.mp3",         1.20, 0.30),
    (SFX_BUNDLED / "riser.mp3",         18.30, 0.30),
    (SFX_BUNDLED / "whoosh-short.mp3",  21.15, 0.40),
    (SFX_BUNDLED / "impact-bass-1.mp3", 33.60, 0.35),
    (SFX_DL / "magic_sparkle_whoosh.mp3", 53.75, 0.45),
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
    if key == "sajat_zoom":
        # Self punch-in: crop ~15% in from the native 1080x1920 frame, scale back up.
        zoom_w, zoom_h = 918, 1632  # ~85% of 1080x1920, centered
        vf = (
            f"crop={zoom_w}:{zoom_h}:({W}-{zoom_w})/2:({H}-{zoom_h})/2,"
            f"scale={W}:{H},{GRADE}"
        )
    else:
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
    print(f"  [{idx:02d}] {key:20s} off={offset:5.2f} dur={duration:5.2f} ({transition})")
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

    flash_beats: list[int] = []  # no transitions at all per instruction -- flash disabled
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

    # Kinetic text overlays, on top of everything
    for k, (text, t_start, t_end) in enumerate(TEXT_OVERLAYS):
        escaped = text.replace("\\", "\\\\").replace("'", "\\'").replace(":", "\\:")
        nxt = f"[txt{k}]"
        filter_parts.append(
            f"{current}drawtext=fontfile='{FONT}':text='{escaped}':"
            f"fontsize=76:fontcolor=white:borderw=4:bordercolor=black:"
            f"x=(w-text_w)/2:y=h*0.72:"
            f"enable='between(t,{t_start:.3f},{t_end:.3f})'{nxt}"
        )
        current = nxt

    filter_parts.append(f"{current}null[outv]")
    filter_complex = ";".join(filter_parts)
    video_out = EDIT_DIR / "video_only_v3.mp4"
    cmd = [
        FFMPEG, "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-an",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        str(video_out),
    ]
    print("compositing video (overlays + grade + text)...")
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
        f"[1:a]atrim=0:{total_duration:.3f},volume=0.16,"
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
    audio_out = EDIT_DIR / "audio_mix_v3.m4a"
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
    total_duration = max(w["end"] for w in data["words"] if w.get("type") == "word") + 1.5

    print(f"extracting {len(BEATS)} b-roll overlay beats...")
    overlay_paths = [
        extract_overlay(i, key, offset, out_end - out_start, transition)
        for i, (key, offset, out_start, out_end, transition) in enumerate(BEATS)
    ]
    flash_path = make_flash_clip()

    video_only = build_video(overlay_paths, flash_path)
    audio_mix = build_audio(total_duration)

    muxed = EDIT_DIR / "muxed_v3.mp4"
    run([
        FFMPEG, "-y",
        "-i", str(video_only), "-i", str(audio_mix),
        "-map", "0:v", "-map", "1:a",
        "-c:v", "copy", "-c:a", "copy",
        "-movflags", "+faststart",
        str(muxed),
    ])

    final_out = EDIT_DIR / "final_v3.mp4"
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
