# zene-dashboard

A gyűjtemény két nézete (idővonal, előadó-gráf) és egy nyitólap egy helyen, egymásra hivatkozva. Az oldal angol nyelvű, világos és sötét témával.

```
python serve.py      # begyűjt + kiszolgál a http://localhost:8766 címen
python build.py      # csak begyűjt
```

Http kell hozzá, nem elég `file://` megnyitni: az idővonal `fetch()`-csel tölti be a
`genre_catalog.json`-t, amit a böngésző `file://` alól CORS miatt megtagad.

## Mi van benne

| fül | forrás | mit mutat |
|---|---|---|
| **Idővonal** | `genre_timeline` | mikor került be mi, műfajonként, kumulált nézetben — 14 831 bejegyzés, 2004-2026 |
| **Előadó-gráf** | `_local_music_graph` | ki kivel szerepel, 19 terület fülenként, előadóra kattintva a mappafája — 15 154 szám |

A nyitólap kártyáin lévő számokat a `build.py` a forrásokból olvassa ki, nem beégetve —
korábban `15,465 bejegyzés` állt rajta, miközben a katalógusban már csak 14 831 sor volt.
Amit nem tud kiolvasni, azt elhagyja, nem találja ki.

## Amit ez a repó **nem** csinál

Nem írja át a két dashboardot. Mindegyik pontosan úgy néz ki és úgy működik, ahogy a
saját forrásában — az egyetlen beavatkozás egy `position:fixed` navigációs pirula a jobb
felső sarokban (Home / Timeline / Artist graph / Light-Dark kapcsoló), ami nem nyúl bele a lap
elrendezésébe.

## Közös téma

A színek, a lapkeret és a navigációs pirula a repó gyökerében lévő `theme.css`-ből jönnek, a
téma betöltését és a kapcsolót a `theme.js` adja. Mindhárom oldal (nyitólap, idővonal,
gráf) ezeket köti be (`../theme.css`, `../theme.js`), a `build.py` pedig a `docs/` gyökerébe
másolja őket, így a hivatkozás a forrásmappákból és a publikált másolatból is érvényes.
A választás `localStorage`-ban él (`zene-theme`), a három oldal közös; ha nincs mentett
választás, a rendszerbeállítás dönt. Az idővonal grafikonjai a `zene-theme` eseményre
újrarajzolódnak.

A tartalom **generált**: a `build.py` mindig a `timeline/` és a `graph/` aktuális kimenetét másolja
be. Ha ott újraépül valami, itt elég egy `python build.py`. Kézzel ezekben a mappákban
semmit nem érdemes szerkeszteni, mert a következő build felülírja.

## Miért 14 831 az egyik és 15 154 a másik

A két szám nem ugyanazt a halmazt írja le, és a különbség teljesen elszámolható
(ellenőrizve 2026-08-11):

```
14 831  idővonal (genre_catalog.json)
  +325  a gráfban van, az idővonalban nincs
        262 .m4a, 47 .wma, 15 .wav — az idővonal csak .mp3-at katalogizál
        1 .mp3 — a `bizarring` kulcsszavas tiltólista, amit a gráf nem ismer
    -1  az idővonalban van, a gráfban nincs
        `_other/call of duty 2 hunidegbeteg.mp3` — közvetlenül az `_other/` alatt ül,
        nem esik egyetlen gráf-terület alá sem (ez a katalógus `other: 1` sora)
-------
15 154  gráf (data/*/normalized/songs.json összege)
```

A gráfban **egyetlen szám sincs kétszer** (15 154 sor, 15 154 különböző útvonal). Korábban
14 igen: a `hungarian` és a `magyar` terület ugyanarra a 14 fájlra tartott igényt az
`_other/_magyar/_cigany` fában. 2026-08-11-én átkerültek a `_magyar rap/G.w.M/` és
`_magyar rap/Teswér/` mappákba — egy előadó, egy hely.

## Források

- `zene-genre-timeline` — `genre_timeline/`
- `zene-local-music-graph` — `_local_music_graph/`
