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
| **Idővonal** | `genre_timeline` | mikor került be mi, műfajonként, kumulált nézetben — 15,459 szám, 2004-2026 |
| **Előadó-gráf** | `_local_music_graph` | ki kivel szerepel, tíz terület fülenként, előadóra kattintva a mappafája |
| **Audio profilok** | `_elektro_classifier` | az audióból kinyert metrikák: trackenkénti profil, stílusok, változó-referencia, térkép |

## Amit ez a repó **nem** csinál

Nem írja át a három dashboardot. Mindegyik pontosan úgy néz ki és úgy működik, ahogy a
saját repójában — az egyetlen beavatkozás egy `position:fixed` navigációs pirula a jobb
felső sarokban, ami nem nyúl bele a lap elrendezésébe. Az idővonal teljes szélességű
grafikonja és a gráf 21 füle érintetlen.

A tartalom **generált**: a `build.py` mindig a másik két repó aktuális kimenetét másolja
be. Ha ott újraépül valami, itt elég egy `python build.py`. Kézzel ezekben a mappákban
semmit nem érdemes szerkeszteni, mert a következő build felülírja.

## Lefedettség

Az idővonal és a gráf a **teljes gyűjteményt** fedi (15,459 szám). Az audio profilok
egyelőre csak az `_other/_elektro` fát (**1,148 track**) — a többi műfajra még nem futott
le a feature-kinyerés. A `_elektro_classifier/extract_features.py` képes rá, mérve ~0.40
track/s a 120 másodperces mintával, tehát a rendezett gyűjtemény (15,564 fájl) ~11 óra.

## Források

- `zene-genre-timeline` — `genre_timeline/`
- `zene-local-music-graph` — `_local_music_graph/`
- audio elemzés — `_elektro_classifier/` (a `zene` munkakönyvtárban, még nincs saját repója)
