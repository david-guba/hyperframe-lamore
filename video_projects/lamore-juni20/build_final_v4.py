"""Build FINAL v4: content-safety fix on top of v3.

Changes from v3, per explicit instruction:
  - "irritalt_bor" (leg-rubbing footage) is no longer used anywhere. The
    juni20 script never actually says "izuleti gyulladas" (joint
    inflammation) -- it's about general/systemic chronic inflammation --
    so the exception clause never applies and the clip drops out entirely.
  - Chronic inflammation must NOT share a visual with that leg-rub clip;
    market positioning is systemic health, not joint pain.
  - "amikor elvagod az ujjadat" (cut-your-finger line) now uses a new,
    literal wound-care clip instead of the leg-rub footage.
  - The other former irritalt_bor slot (~35s, "tartja a szervezetedet")
    now uses a third kronikus_gyulladas segment instead, keeping the
    visual on-message with the systemic-inflammation positioning.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import lamore_config as cfg  # noqa: E402

FFMPEG = cfg.FFMPEG
FFPROBE = cfg.FFPROBE

PROJECT = Path(__file__).resolve().parent
BROLL_DIR = cfg.BROLL_DIR
STOCK_DIR = cfg.STOCK_DIR
SFX_BUNDLED = cfg.SFX_BUNDLED
SFX_DL = PROJECT / "sfx_downloaded"
MUSIC = PROJECT / "music_candidates" / "close_up_michael_ramir_c.mp3"

RAW = PROJECT / "raw.mp4"
TRANSCRIPT = PROJECT / "edit" / "transcripts" / "raw.json"
EDIT_DIR = PROJECT / "edit"
WORK = EDIT_DIR / "overlays_v4"
WORK.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920
GRADE = "eq=contrast=1.06:brightness=0.0:saturation=1.0,curves=master='0/0 0.25/0.23 0.75/0.77 1/1'"

SOURCES = {
    "mozgashiany_combo": BROLL_DIR / "mozgáshiány + rossz táplálkozás.mp4",
    "fejfajas": BROLL_DIR / "fejfájás.mp4",
    "elegtelen_alvas": BROLL_DIR / "elégtelen alvás.mp4",
    "lamore_termekek": BROLL_DIR / "Lamore termékek.MOV",
    "lamore_termekek2": BROLL_DIR / "Lamore termékek.mp4",
    "omega": BROLL_DIR / "omega zsírsavak.mp4",
    "flavonoid": BROLL_DIR / "antixoidáns és flavonoid.mp4",
    "kronikus_gyulladas": BROLL_DIR / "krónikus gyulladás.mp4",
    "immunrendszer": BROLL_DIR / "immunrendszer.mp4",
    "stresszes_ember": BROLL_DIR / "stresszes ember.mp4",
    "rossz_taplalkozas": BROLL_DIR / "rossz táplálkozás.mp4",
    "sportolas": BROLL_DIR / "sportolás.mp4",
    "egeszseges_taplalkozas": BROLL_DIR / "egészséges táplálkozás.mp4",
    "pihenteto_alvas": BROLL_DIR / "pihentető alvás.mp4",
    "stresszes_no2": STOCK_DIR / "stresszes_no_halanteka.mp4",
    "kanapen_no": STOCK_DIR / "kanapen_fekvo_no.mp4",
    "seb_kotozes": STOCK_DIR / "ujj_sebtapasz.mp4",
    # New, each used exactly once -- no clip repeats anywhere in this edit,
    # and none of them are leg/knee-touching visuals (that whole motif is
    # retired; "izuleti" and "terdmasszazs" are gone for good).
    "vervesejtek": STOCK_DIR / "vervesejtek.mp4",
    "sejt_animacio_kek": STOCK_DIR / "sejt_animacio_kek.mp4",
    "immunsejt_kozeli": STOCK_DIR / "immunsejt_kozeli.mp4",
    "sejt_forgo_3d": STOCK_DIR / "sejt_forgo_3d.mp4",
    "sejt_kek_lila": STOCK_DIR / "sejt_kek_lila.mp4",
    "sejt_lila": STOCK_DIR / "sejt_lila.mp4",
    "faradt_no_munkahelyen": STOCK_DIR / "faradt_no_munkahelyen.mp4",
    "almatlansag": STOCK_DIR / "almatlansag.mp4",
    "unott_no_kanapen2": STOCK_DIR / "unott_no_kanapen2.mp4",
}

# (source_key, offset_in_source, output_start, output_end, transition)
# Every source below appears in exactly ONE beat -- no clip is reused,
# per instruction. "izuleti"/"terdmasszazs" (leg-rub-style visuals) are
# gone entirely since the script never says "ízületi gyulladás".
BEATS = [
    ("kronikus_gyulladas",       0.00,  3.02,  5.34, "flash"),   # opening reveal
    ("seb_kotozes",              1.00,  8.32, 10.38, "cut"),     # "elvágod az ujjadat"
    ("sejt_kek_lila",            0.00, 12.34, 13.62, "cut"),     # "Így dolgozik a tested"
    ("vervesejtek",              0.00, 13.62, 15.64, "cross"),   # "A probléma a krónikus gyulladás"
    ("immunrendszer",            0.00, 17.68, 19.10, "cut"),
    ("immunsejt_kozeli",         0.00, 19.16, 21.56, "flash"),   # "konkrét seb lenne"
    ("mozgashiany_combo",        0.00, 23.10, 25.06, "cut"),
    ("stresszes_ember",          0.00, 25.22, 26.12, "cross"),
    ("rossz_taplalkozas",        0.00, 26.28, 27.72, "cut"),
    ("elegtelen_alvas",          0.00, 27.78, 28.86, "flash"),
    ("sejt_lila",                0.00, 31.38, 33.04, "cut"),     # "állandó készenlétben"
    ("faradt_no_munkahelyen",    0.00, 33.10, 34.96, "cross"),   # "tartja a szervezetedet"
    ("sejt_animacio_kek",        0.00, 35.02, 36.80, "cut"),     # "energiádat leköti"
    ("almatlansag",              0.00, 36.84, 38.48, "flash"),   # "vagy fáradt egyből"
    ("fejfajas",                 0.00, 39.50, 41.30, "cross"),
    ("unott_no_kanapen2",        0.00, 41.46, 44.18, "cut"),     # "kevés a motivációd"
    ("sportolas",                0.00, 46.14, 48.70, "flash"),
    ("egeszseges_taplalkozas",   0.00, 48.74, 50.12, "cross"),
    ("pihenteto_alvas",          0.00, 50.16, 51.58, "cut"),
    ("lamore_termekek",          0.00, 52.46, 55.08, "flash"),   # BRAND
    ("omega",                    0.00, 55.80, 57.16, "cross"),   # INGREDIENT
    ("flavonoid",                0.00, 57.24, 58.34, "cut"),     # INGREDIENT
    ("sejt_forgo_3d",            0.00, 58.46, 61.00, "cut"),     # "vesznek részt"
    ("stresszes_no2",            0.50, 63.28, 64.52, "cut"),
    ("kanapen_no",               0.50, 64.52, 65.60, "cross"),
    ("lamore_termekek2",         0.00, 65.60, 66.30, "flash"),   # closing brand flash -- different file than the 52.46s one
]

# A-roll ranges kept as gray connective shots: 0-3.02, 5.34-8.32, 10.44-12.34,
# 15.84-17.68, 21.58-23.04, 29.00-31.32, 38.52-39.44, 44.22-46.10 (PIVOT),
# 51.64-52.46, 55.14-55.80, 58.46-61.00, 61.06-63.28 (CTA open). No cuts
# needed there -- it's the raw base itself, always visible under gaps.

# SFX cues: (file, start_time_in_output, volume_multiplier)
SFX_CUES = [
    (SFX_BUNDLED / "riser.mp3",                             1.2,  0.30),
    (SFX_DL / "cinematic_tunnel_reverb_woosh.mp3",          3.00, 0.55),
    (SFX_DL / "cinematic_whoosh_fast_transition.mp3",       8.20, 0.50),
    (SFX_BUNDLED / "whoosh-short.mp3",                     12.25, 0.40),
    (SFX_DL / "cinematic_whoosh_fast_transition.mp3",      17.60, 0.50),
    (SFX_BUNDLED / "pop.mp3",                              19.10, 0.45),
    (SFX_BUNDLED / "whoosh-short.mp3",                     23.05, 0.40),
    (SFX_BUNDLED / "pop.mp3",                              25.20, 0.35),
    (SFX_BUNDLED / "whoosh-short.mp3",                     26.25, 0.40),
    (SFX_BUNDLED / "pop.mp3",                              27.70, 0.40),
    (SFX_BUNDLED / "impact-bass-1.mp3",                    31.35, 0.40),
    (SFX_BUNDLED / "whoosh-short.mp3",                     35.00, 0.40),
    (SFX_BUNDLED / "pop.mp3",                              36.80, 0.40),
    (SFX_DL / "cinematic_trailer_riser.mp3",               41.60, 0.45),
    (SFX_DL / "cinematic_tunnel_reverb_woosh.mp3",         43.90, 0.55),
    (SFX_DL / "magic_sparkle_whoosh.mp3",                  46.05, 0.50),
    (SFX_BUNDLED / "whoosh-short.mp3",                     48.70, 0.35),
    (SFX_DL / "positive_notification.mp3",                 52.40, 0.55),
    (SFX_BUNDLED / "whoosh-short.mp3",                     55.75, 0.35),
    (SFX_BUNDLED / "whoosh-short.mp3",                     58.40, 0.35),
    (SFX_BUNDLED / "whoosh-short.mp3",                     63.25, 0.40),
    (SFX_DL / "happy_bells_notification.mp3",              65.50, 0.55),
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
    video_out = EDIT_DIR / "video_only_v4.mp4"
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
    inputs: list[str] = ["-i", str(RAW)]          # 0: narration
    inputs += ["-i", str(MUSIC)]                   # 1: music
    for f, _t, _v in SFX_CUES:
        inputs += ["-i", str(f)]                   # 2..N: sfx

    filter_parts: list[str] = []
    fade_start = max(0.0, total_duration - 1.5)
    filter_parts.append(
        f"[1:a]atrim=0:{total_duration:.3f},volume=0.20,"
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
    audio_out = EDIT_DIR / "audio_mix_v4.m4a"
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

    muxed = EDIT_DIR / "muxed_v4.mp4"
    run([
        FFMPEG, "-y",
        "-i", str(video_only), "-i", str(audio_mix),
        "-map", "0:v", "-map", "1:a",
        "-c:v", "copy", "-c:a", "copy",
        "-movflags", "+faststart",
        str(muxed),
    ])

    final_out = EDIT_DIR / "final_v4.mp4"
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
