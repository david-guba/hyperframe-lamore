# Lamore videó vágás — workflow és kreatív szabályok

> Az itt leírt szabályokat a "Guba videó vágás" (homoktövis talking-head reklám)
> és a "Lamore vid juni 6" videók vágása közben dolgoztuk ki. Minden jövőbeli
> Descript-es videóvágásnál ezt kell követni.

---

## 1. TECHNIKAI WORKFLOW (Descript MCP)

### Import — csak Google Drive linkkel megbízható
A `import_media` tool **direkt fájlfeltöltése** (content_type + file_size,
PUT upload_url-re) **megbízhatatlanul, "Import failed" hibával fut el** —
függetlenül a fájlmérettől, és többszöri újrapróbálkozással sem javul.

**Megoldás — mindig ezt használd:**
1. Töltsd fel a fájlt Google Drive-ra a `gws` CLI-vel:
   ```
   gws drive files create --params '{"fields":"id,name,webViewLink"}' \
     --json '{"name":"<fájlnév>"}' --upload "<lokális útvonal>" \
     --upload-content-type "video/mp4"   # vagy video/quicktime .mov-hoz
   ```
2. Tedd publikusan elérhetővé:
   ```
   gws drive permissions create --params '{"fileId":"<ID>"}' \
     --json '{"role":"reader","type":"anyone"}'
   ```
3. Importáld a kapott `webViewLink`-et a Descript `import_media` tool
   `url` paraméterébe.

### AI-ügynök (Underlord / prompt_project_agent)
- Minden hívás **AI-kreditet** használ (a Free plan kerete kevés — egy nagyobb,
  több lépéses kérés félbeszakadhat "Insufficient AI credits" hibával).
- Bontsd több, kisebb, célzott promptra a nagy kéréseket, hogy ha elfogy a
  kredit, ne vesszen el a teljes munka.
- A `prompt_project_agent` végső `agent_response`-a néha csak az **utolsó**
  apró javítást írja le, nem a teljes elvégzett munkát — mindig ellenőrizd
  `get_project`-tel, milyen új médiák/változások kerültek be.

### Manuális (computer-use) vágás, ha elfogy a kredit
- A Descript desktop appban drag&drop-pal a Project/Stock Media panelből
  közvetlenül a **felső scene-thumbnail sorra** húzva lehet egy klipet egy
  adott jelenethez rendelni — ez megbízhatóan csak azt a jelenetet írja át.
- **FONTOS**: drag előtt/közben figyeld a "Selected in: Current scene |
  All scenes" választót — ha nincs "Current scene"-re állítva, a módosítás
  **az összes jelenetre szétterjedhet**, ami ugyanazt a klipet használja
  (ez többször előfordult, és sok másodpercnyi, nem kívánt egyforma képet
  eredményezett).
- **SOHA ne nyomj Backspace/Delete-et egy kiválasztott scene-chipen** — ez
  törli a hozzá tartozó **elhangzott szöveget/jelenetet** a szkriptből!
  Helyette: jobbklikk a timeline-klipen → **"Delete"** a context menüből —
  ez csak a vizuális réteget törli, a szöveg/hang marad.
- Vágás: playhead pontos pozicionálása + "Split" gomb/`S` billentyű, majd a
  kívánt klip drag&drop a két vágási pont közé.

---

## 2. KREATÍV VÁGÁSI SZABÁLYOK

### Ritmus
- **Egyetlen snitt (A-roll VAGY B-roll) se legyen hosszabb 3 másodpercnél.**
  Ha egy mondat hosszabb, vágj bele b-rollt vagy válts vissza A-rollra.
- **Ugyanaz a B-roll klip ne ismétlődjön 2 egymást követő snittben.** Ha a
  következő mondat is ugyanazt a vizuált indokolná, inkább válts A-rollra
  közte, és csak utána térj vissza (vagy használj egy másik, releváns klipet).

### B-roll illesztés — szó szintű pontossággal
- A b-roll **pontosan az adott szó elhangzásakor** induljon, ne csússzon el
  1-2 másodperccel előre/hátra (ez volt a leggyakoribb hiba).
- **Márkanév/saját termék említésénél** ("L'amore Homoktövis" stb.) mindig a
  **saját termékes felvétel** (pl. `Lamore termékek.MOV`) menjen, SOHA
  generikus stock.
- **Összetevő/hatóanyag említésénél** (C-vitamin, omega-7, flavonoid,
  antioxidáns) az adott összetevőre jellemző vizuál (vitamin/citrus, lazac,
  bogyós gyümölcs) — szó szintű igazítással.
- **Test/szervezet leírásánál** ("a tested", "sejtjeid", "krónikus gyulladás",
  "védekezés") **TEST/BIOLÓGIA vizuál** kell (vérsejt, gyulladásos
  ízület/fájdalom, immunrendszer, energikus testmozgás) — **NEM gyümölcsös/
  bogyós kép**. A gyümölcs/bogyó csak az összetevő-említésnél jó, nem a
  szervezet leírásánál.
- **Variáld a test-vizuálokat is** — ne ugyanaz a mikroszkópos sejt-klip
  menjen minden testtel kapcsolatos ponton; rotálj több klip között
  (pl. fehérvérsejt más szögből, ízületi gyulladás, energikus testmozgás).

### Áttünetek — variáld, ne legyen monoton
- **Ne csak egyféle áttünetet (pl. zoom-blur) használj egész végig** — ez
  monotonná, zavaróan ismétlődővé válik. Keverj bele más stílusú átmeneteket
  is (pl. **shake/rázás**, crossfade, clock wipe stb.), és ne legyen
  2-3 egymást követő vágásnál ugyanaz az áttünés-típus.

### Több B-roll érzések/hangulatok kiemelésére
- Ahol a szöveg egy **érzést/hangulatot** ír le (pl. "stresszes időszak",
  "fáradtság", "leterheltség", "motivációhiány"), ne csak **egy** b-roll
  kép menjen hosszan — illessz be **2-3 különböző, releváns vizuált gyors
  egymásutánban** (akár 1-1.5 másodperces snittekkel), hogy a pörgés magát
  az érzést is átadja. (Pl. "stresszes időszak": stresszes arc → óra/
  időnyomás → halmozódó munka, gyors váltásokkal.)
- Ez nem írja felül az alapszabályokat: itt is figyelni kell, hogy **ne
  ismétlődjön 2 egymást követő snittben ugyanaz a klip**, és **egyik snitt
  se legyen hosszabb 3 másodpercnél** (itt inkább rövidebb, 1-1.5s snittek
  jók a pörgéshez).

### Hangeffektek és zene
- **Ár/szám említésénél** rövid figyelemfelkeltő SFX (pl. "cash register"
  cha-ching hang).
- **Háttérzene**: alacsony hangerő (kb. 15-25%), automatikus ducking a
  beszéd alatt.
- ⚠️ **Ducking csapda**: ha a ducking minden háttérhangot (zenét ÉS SFX-et is)
  lenyom beszéd alatt, és az SFX épp beszéddel egy időben szól (pl. az ár
  elhangzásakor), az SFX hallhatatlanná válhat. Ha ez történik, vagy emeld
  fel külön az SFX gain-jét (~70-90%), vagy vedd ki a ducking hatása alól.

### Formátum
- **9:16, teljesen kitöltött vászon** — sehol ne legyen fekete sáv. Ha
  valahol marad fekete csík, valószínűleg egy jelenet pozíció/crop értéke
  (`y` offset) van elcsúszva — ezt kell középre/kitöltésre igazítani.

---

## 3. ITERATÍV FOLYAMAT

1. Első AI-agent pass: alap vágás (töltelékszó-eltávolítás, kezdeti b-roll,
   áttünések, alapzene).
2. Manuális vagy AI-agent ellenőrzés: szó-illesztés, 3 mp-es szabály,
   egymás-melletti duplikáció, hangerők, formátum.
3. Pontos, idézett szavakkal/időbélyegekkel megadott javító promptok —
   minél konkrétabb az utasítás (melyik szónál mi menjen), annál pontosabb
   az eredmény.
4. Ismételd, amíg a teljes kompozíció megfelel a fenti szabályoknak.

---

## 4. HYPERFRAMES / VIDEO-USE PIPELINE (Claude Code, nem Descript)

> A "Lamore vid juni#20" és "Lamore vid juni#21" videók vágása közben
> kidolgozott szabályok, amikor a vágás nem Descripten, hanem a
> Hyperframes + video-use (Claude Code, ffmpeg overlay-architektúra)
> pipeline-on keresztül történik. A 2. fejezet kreatív szabályai
> (ritmus, B-roll illesztés, áttünés-variálás) itt is érvényesek.

### Tervezés és jóváhagyás
- **Minden új nyers videónál előbb írásos tervet kérünk** (másodpercre
  lebontva: mit mond a szöveg, milyen A-roll/B-roll megy oda, milyen
  átmenet) — csak jóváhagyás után indul a tényleges vágás.
- **Vizuális idővonal-ábrát** is kérünk a kompozícióról (A-roll/B-roll
  kategóriák színezve, SFX-jelölőkkel) — nem elég a szöveges táblázat.
- Az SFX-tervet is **külön átbeszéljük**, mielőtt a végleges vágás elindul.

### B-roll könyvtár — ellenőrizd, hogy illik-e a témához
- **Ne feltételezd, hogy a meglévő B-roll könyvtár univerzálisan
  használható** — más témájú videóhoz (pl. egészségtünet-edukáció vs.
  gazdaság/eredettörténet) teljesen más B-roll kell. Mielőtt tervet
  írsz, nézd át, illik-e egyáltalán a meglévő anyag az új szöveghez.
- Ha a felhasználó saját felvételt ad (pl. ültetvény, szüret,
  termékasztal), **azt kell elsőként használni**, nem a generikus stockot.
- **Nem kötelező minden mondathoz B-roll** — bizonyos állításoknál
  szándékosan A-roll is maradhat, ha nincs hozzá jó vizuál, vagy a
  felhasználó úgy dönt (pl. "hidegen préseljük", "csak és kizárólag").
- **Castingszabály stockhoz**: ha egy klipen egyetlen ember látható, az
  40 körüli, fehér nő legyen (hacsak a felhasználó másképp nem szól).

### Zene és SFX beszerzés
- **Zenét a felhasználó keres**, az asszisztens csak specifikációt ad
  (hangulat-ív, BPM, hangszerelés, hossz) — nem tölt le kész zenét
  saját döntésből.
- **SFX-et viszont az asszisztens kereshet és tölthet le** a netről
  (Mixkit/Pixabay-szerű, kereskedelmi felhasználásra jogtiszta
  forrásból), ha erre kifejezett engedélyt kap.
- **A záró jelenetnél nem kötelező SFX** — néha jobb, ha a záró B-roll
  (pl. termékfogyasztás) simán, hangkiemelés nélkül fut.

### Technikai buktatók (ffmpeg overlay-architektúra)
- **Minden snitt ≤3 másodperc legyen — az A-roll "kötőszövet" szakaszok
  között is.** Az overlay-architektúrában két egymást követő A-roll
  szakasz (nincs köztük B-roll overlay) vizuálisan EGY folytonos snittnek
  számít, akkor is, ha a tervben külön sornak lettek felírva. Mindig
  ellenőrizd, nincs-e két szomszédos A-roll-gap, ami összeadva 3mp fölé
  megy — ha igen, vágj bele egy rövid B-roll-t.
- **Ne közelíts rá (crop/zoom) B-roll-ra, ha az már natívan 9:16.** Ha egy
  forrásklip zoomolva/túlvágva jelenik meg a végeredményben, először
  ellenőrizd `ffprobe`-bal a `rotation` side-data mezőt — előfordult, hogy
  egy fájl elforgatás-metaadattal (pl. `rotate=90`) landscape
  (pl. 3840x2160) nyers pixelméretet jelentett, miközben a valódi,
  megjelenített tartalom portré (9:16) volt. A crop-számítás emiatt rossz
  értékekkel dolgozott, és az eredmény indokolatlanul be lett zoomolva.
  Megoldás: vagy a forrásfájlt exportáld helyesen tájolt (natív 9:16)
  verzióban, vagy a crop-logikát tedd forgatás-tudatossá.
- B-roll klipeknek gyakran **nincs saját hangsávjuk** — ilyenkor a B-roll
  csak vizuális overlay a folytonos narráció fölött, nem vágja meg a
  hangot. Ha van saját hangsávja (pl. termékes felvétel), azt némítsd le,
  hogy ne zavarja a narrációt.

---

*Dokumentum verziója: 2.0 — a "Guba videó vágás", "Lamore vid juni 6",
"Lamore vid juni#20" és "Lamore vid juni#21" projektek tanulságai alapján.*
