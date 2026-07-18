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
100MB/fájl limit).

## Beállítás egy új gépen / felhőben

A szkriptek most a `lamore_config.py`-n keresztül oldják fel az útvonalakat
(környezeti változó > repó-relatív `assets/` mappa > az eredeti Windows-gép
alapértelmezése). Nincs szükség kézi szerkesztésre — csak tedd az assetokat
a megfelelő helyre, vagy állítsd be a környezeti változókat:

1. **ffmpeg / ffprobe**: legyenek a PATH-on (vagy állítsd be `FFMPEG_BIN` /
   `FFPROBE_BIN` env változót egy konkrét elérési útra).
2. **B-roll könyvtár**: töltsd le a Drive-ról a `videó anyagok` mappát, és
   tedd a repo `assets/broll/` alá (a `stock_candidates` almappával együtt),
   vagy állítsd be a `LAMORE_BROLL_DIR` env változót a tényleges helyére.
3. **Bundled SFX** (whoosh/riser/pop/stb.): tedd az `assets/sfx_bundled/`
   alá, vagy állítsd be `LAMORE_SFX_BUNDLED_DIR`-t.
4. **Megosztott zene/SFX** (amit a juni17/juni21 a juni20 mappájából
   használ): ha máshova teszed a juni20 projektet, állítsd be
   `LAMORE_SHARED_ASSETS_DIR`-t a helyére.

Minden env változó opcionális — ha üresen hagyod, a szkript a repó-relatív
`assets/` mappát próbálja először, csak ez után esik vissza az eredeti
Windows-gép elérési útjaira.

**Ismert korlátozás**: a `lamore-juni17/build_final.py` a Windows Arial Bold
betűtípust hivatkozza közvetlen elérési úttal (`C:/Windows/Fonts/arialbd.ttf`)
a "Hippophae" / "2000+ ÉV" feliratokhoz — Linux-alapú felhő-környezetben ezt
egy elérhető `.ttf` fájl útvonalára kell cserélni.

Szükséges eszközök a futtatáshoz: ffmpeg, Python 3.12+ (lásd
`requirements` — nincs pip-csomag függőség, csak stdlib).
