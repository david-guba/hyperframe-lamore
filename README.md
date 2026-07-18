# hyperframe-lamore

Vágó-szkriptek és munkafolyamat-dokumentáció a Lamore homoktövis videósorozathoz
(Hyperframes + video-use overlay-architektúra, ffmpeg-alapú).

## Tartalom

- `video_projects/lamore-juni17/build_final.py` — homoktövis-történelem videó
- `video_projects/lamore-juni20/build_final_v4.py` — krónikus gyulladás / egészség videó
- `video_projects/lamore-juni21/build_final.py` — eredettörténet (földtől az asztalig) videó
- `video-vagas-workflow.md` — kreatív és technikai szabálygyűjtemény
- `CLAUDE.md` — projekt-kontextus és pipeline leírás

## Fontos

**A nyers videók, B-roll klipek és renderelt kimenetek szándékosan NINCSENEK
a repóban** — ezek Google Drive-on vannak tárolva (túl nagyok GitHub-hoz,
100MB/fájl limit). A szkriptek jelenleg **abszolút Windows elérési utakat**
tartalmaznak (`E:\CLAUDE VIDEO EDIT\...`, `C:\Users\User\...`) — felhőben
vagy más gépen futtatáshoz ezeket az útvonalakat át kell írni a tényleges
médiafájlok helyére.

Szükséges eszközök a futtatáshoz: ffmpeg, Python 3.12+.
