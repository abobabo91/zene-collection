# zene-dashboard

A gyűjtemény három nézete egy helyen, egymásra hivatkozva.

```
python serve.py      # begyűjt + kiszolgál a http://localhost:8766 címen
python build.py      # csak begyűjt
```

Http kell hozzá, nem elég `file://` megnyitni: az idővonal `fetch()`-csel tölti be a
`genre_catalog.json`-t, amit a böngésző `file://` alól CORS miatt megtagad.

## Mi van benne

| fül | forrás | mit mutat |
|---|---|---|
| **Idővonal** | `genre_timeline` | mikor került be mi, műfajonként, kumulált nézetben — 14 975 bejegyzés, 2004-2026 |
| **Előadó-gráf** | `_local_music_graph` | ki kivel szerepel, 19 terület fülenként, előadóra kattintva a mappafája — 15 299 szám |
| **Audio profilok** | `_elektro_classifier` | az audióból kinyert metrikák: trackenkénti profil, stílusok, változó-referencia, térkép |

A nyitólap kártyáin lévő számokat a `build.py` a forrásokból olvassa ki, nem beégetve —
korábban `15,465 bejegyzés` állt rajta, miközben a katalógusban már csak 14 975 sor volt.
Amit nem tud kiolvasni, azt elhagyja, nem találja ki.

## Amit ez a repó **nem** csinál

Nem írja át a három dashboardot. Mindegyik pontosan úgy néz ki és úgy működik, ahogy a
saját repójában — az egyetlen beavatkozás egy `position:fixed` navigációs pirula a jobb
felső sarokban, ami nem nyúl bele a lap elrendezésébe. Az idővonal teljes szélességű
grafikonja és a gráf 21 füle érintetlen.

A tartalom **generált**: a `build.py` mindig a másik két repó aktuális kimenetét másolja
be. Ha ott újraépül valami, itt elég egy `python build.py`. Kézzel ezekben a mappákban
semmit nem érdemes szerkeszteni, mert a következő build felülírja.

## Lefedettség

Az idővonal és a gráf a **teljes gyűjteményt** fedi. Az audio profilok egyelőre csak az
`_other/_elektro` fát (**1 216 track a 15 313-ból**) — a többi műfajra még nem futott le a
feature-kinyerés, tehát ez a fül messze nem egyenrangú a másik kettővel. A
`_elektro_classifier/extract_features.py` képes rá, mérve 0.45 track/s a 120 másodperces
mintával 6 workerrel, tehát a maradék ~14 100 fájl nagyjából 9 óra.

Egy track hibázik az elemzőn: `trance_dance_rave/house_classics/Duck Sauce - Barbra
Streisand (Original Mix).mp3`.

## Miért 14 975 az egyik és 15 299 a másik

A két szám nem ugyanazt a halmazt írja le, és a különbség teljesen elszámolható
(ellenőrizve 2026-08-11):

```
14 975  idővonal (genre_catalog.json)
  +325  a gráfban van, az idővonalban nincs
        262 .m4a, 47 .wma, 15 .wav — az idővonal csak .mp3-at katalogizál
        1 .mp3 — a `bizarring` kulcsszavas tiltólista, amit a gráf nem ismer
    -1  az idővonalban van, a gráfban nincs
        `_other/call of duty 2 hunidegbeteg.mp3` — közvetlenül az `_other/` alatt ül,
        nem esik egyetlen gráf-terület alá sem (ez a katalógus `other: 1` sora)
-------
15 299  gráf (data/*/normalized/songs.json összege)
```

A gráfban **egyetlen szám sincs kétszer** (15 299 sor, 15 299 különböző útvonal). Korábban
14 igen: a `hungarian` és a `magyar` terület ugyanarra a 14 fájlra tartott igényt az
`_other/_magyar/_cigany` fában. 2026-08-11-én átkerültek a `_magyar rap/G.w.M/` és
`_magyar rap/Teswér/` mappákba — egy előadó, egy hely.

## Források

- `zene-genre-timeline` — `genre_timeline/`
- `zene-local-music-graph` — `_local_music_graph/`
- audio elemzés — `_elektro_classifier/` (a `zene` munkakönyvtárban, még nincs saját repója)
