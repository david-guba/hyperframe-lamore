# Video editing studio

This is Nate Herkelman's Claude Code video-editing pipeline: drop a raw clip in, get it trimmed and motion-graphics'd out.

## Pipeline

1. **video-use** (`video-use/`, skill symlinked at `.claude/skills/video-use`) — transcribes locally with `faster-whisper` (no API key, no cost — first run per model size downloads weights from Hugging Face and caches them), removes filler words/retakes/dead air, color grades, burns subtitles. No speaker diarization in this local setup.
2. **HyperFrames** (`hyperframes/`, 20 skills symlinked at `.claude/skills/hyperframes*`) — writes motion graphics as plain HTML, renders to MP4, synced to word-level timestamps from the transcript.

Router skill: `/hyperframes` picks the right domain skill for any "make me a video" request.

## Workflow

- Put raw footage in a project folder under `video_projects/<project-name>/`.
- Say "edit this into a video" — video-use trims filler words/retakes first (confirm the cut plan before it executes).
- Then describe the motion graphics beat by beat (what appears, when, what it says) — HyperFrames plans beats with timestamp anchors, you approve/revise before it builds HTML.
- All outputs land in `<videos_dir>/edit/` — never inside `video-use/` or `hyperframes/` themselves.

## Requirements status

- Node.js 24.18.0 — OK (HyperFrames needs 22+)
- FFmpeg 8.1.2 — installed via winget (`Gyan.FFmpeg`), not yet on this machine's PATH — restart terminal after setup, or use the full path under `%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin`
- Python 3.12.10 — installed via winget, not yet on PATH — restart terminal
- video-use Python deps — installed (`requests`, `librosa`, `matplotlib`, `pillow`, `numpy`, `faster-whisper`)
- Transcription — patched to use local `faster-whisper` (CPU, int8, default model `small`) instead of ElevenLabs Scribe. No API key needed, runs fully offline after the first model download. No speaker diarization. See `video-use/helpers/transcribe.py`.

## Note

Restart your terminal / Claude Code session once after this setup so FFmpeg and Python are picked up on PATH.
