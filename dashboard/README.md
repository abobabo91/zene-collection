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

## A számok egyeznek

Mérve 2026-10-08: gráf, idővonal-katalógus és CSV egyaránt **15 369** (nincs duplikált sor).
A három ugyanazt a szűrést használja: `buildkit.is_blocked` / `BLOCKLIST_KEYWORDS`. Régebben
mindegyik a saját listáját vezette, így a gráf 15 370-et, a katalógus 15 369-et mutatott.
Az idővonal "Total songs" kártyája 15 363, amíg a tartomány 2004-01-től indul (6 fájl 1999 és
2002 közötti); ilyenkor a címke "Songs in range (6 outside)".

## Források

- `zene-genre-timeline` — `genre_timeline/`
- `zene-local-music-graph` — `_local_music_graph/`
