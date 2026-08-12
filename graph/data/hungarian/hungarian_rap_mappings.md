# Hungarian Rap/Trap Mappings

The editable structure for the Hungarian local music graph pass. Same section format as
`us_rap_trap_mappings.md`, so both areas are parsed by the same loader.

Purpose:

- capture artist aliases and spelling normalization
- define groups and crews
- define labels and roster membership
- record the home town of an artist, which in this area is curated rather than derived

Unlike the US area, region does **not** come from the folder tree - `_magyar rap` and
`_magyar trap` are sorted by artist, not by city. Region lives on the person, in the
`region:` field of a Person entry, and on the group in `## Group regions`.

## Alias normalization

Format:

`canonical: alias 1, alias 2`

One line per canonical name. A second line with the same canonical name does **not**
merge - the later line silently replaces the earlier one.

- `Deego: Diggieman`
- `K8: Kolg8eight`
- `SÉF: Sör és Fű`
- `The Steve: Steve Antal`
- `Turha: Február`

## Groups

Format:

`Group Name: member 1, member 2`

A group with no members listed is one whose line-up is not resolved yet; it still exists
as an entity and its songs are still credited to it.

- `AK26: Giajenno, Hiro`
- `Akkezdet Phiai: Saiid, Újonc Peti`
- `Alakváltók: Artoscsaba, Siska Finuccsi`
- `Az Idő Urai: Bankos, Nos'chez, Zenk`
- `Barbárfivérek: Deego, Tibbah`
- `BeatMarket: Essemm, Ra`
- `BKP: `
- `Bruno X Spacc: Bruno, Spacc`
- `BSW: Gaben, Mettyú`
- `Dreamerz: San, Tkyd`
- `DSP: Bom, Dipa`
- `Egyenlők: Ketioz, Phat, Rambo, Siska Finuccsi`
- `Fattyúk: `
- `Fhészek: Odupla, The Steve`
- `Furakor: Akr, Fura Csé`
- `Ganxsta Zolee és a Kartel: `
- `Gruppen Family: Eckü, Siska Finuccsi`
- `Hősök: Eckü, Mentha`
- `ibbigang: Szalai, Valter`
- `IFS: Filo, Smile of Hell`
- `Jam Balaya: Fullánk, Ketioz, Rambo`
- `Killakikitt: AZA, Tirpa`
- `Káva: Akr, El Magico, Fura Csé, Szimat`
- `Majmok Bolygója: Essemm, Süti`
- `Makaronin: eSGé, Sosa`
- `Nevenincs: `
- `New Fhészek: Odupla, Illegalvoice`
- `NKS: Nos'chez, Zenk`
- `Olvasók A zŰrben: `
- `Pogány Induló: `
- `Punnany Massif: Máté, Wolfie`
- `Rydu: Phat, Tkyd`
- `Samurai Flow: Drezzick, Nomagróf`
- `SÉF: `
- `Teswér: Fiatal Veterán, Hibrid`
- `Vészkijárat: Phat, Siska Finuccsi`
- `Warninshotz: `
- `Weszélyes Elemek: `

## Labels

Format:

`Label Name: artist 1, artist 2`

Groups signed to a label are listed in the group members' own entries, not here.

- `AuthenticBeats Records: Authentic Beats, night rainbow, P_s`
- `Bloose Broavaz: Bom, Chump_Yanz, Deego, Dipa, Drezzick, Eckü, Landi, Nomagróf, Phat, Rizkay, San, Siska Finuccsi, Tibbah, Tkyd`
- `Criminal: Bankos, Norba, Nos'chez, Zenk`
- `Garage: Akr, El Magico, Essemm, Frog, Fura Csé, Ra, Szimat, Süti`
- `goldsoul: C2SH, Kuli†King, P.G., Rico`
- `IFS: Filo, Smile of Hell`
- `RTM: Awful, Déó, Giajenno, Hiro, Kamikaze, Mr.Busta, redOne`
- `SCBP: AZA, KalashniKnow, PKO, Shuka, Tactica, Tezsviir, Tirpa, Turha`
- `Vicc Beatz: Dirty, Fullánk, Ketioz, Kontroll, Lalipop, Marabela, Miss Business, Rambo`

## Group labels

Format:

`Group Name: label`

Carried explicitly, **not** derived from the members' labels. `Nevenincs` is a goldsoul
act with no member list, so deriving would drop its label and its 13 songs; `Hősök` and
`Gruppen Family` would gain a Bloose Broavaz tag they never had, just because one member
is signed there.

- `AK26: RTM`
- `Az Idő Urai: Criminal`
- `Barbárfivérek: Bloose Broavaz`
- `BeatMarket: Garage`
- `Dreamerz: Bloose Broavaz`
- `DSP: Bloose Broavaz`
- `Egyenlők: Bloose Broavaz, Vicc Beatz`
- `Furakor: Garage`
- `IFS: IFS`
- `Jam Balaya: Vicc Beatz`
- `Killakikitt: SCBP`
- `Káva: Garage`
- `Majmok Bolygója: Garage`
- `Nevenincs: goldsoul`
- `NKS: Criminal`
- `Rydu: Bloose Broavaz`
- `Samurai Flow: Bloose Broavaz`
- `Vészkijárat: Bloose Broavaz`

## Group regions

Format:

`Group Name: town`

The home town of a crew, where it is not simply the town of every member.

- `AK26: Surány`
- `Akkezdet Phiai: Budapest`
- `Barbárfivérek: Győr`
- `BSW: Somogy`
- `DSP: Budapest`
- `Egyenlők: Győr`
- `Fattyúk: Tatabánya`
- `Furakor: Tatabánya`
- `Hősök: Veszprém`
- `IFS: Szeged`
- `Jam Balaya: Győr`
- `Killakikitt: Budapest`
- `Káva: Tatabánya`
- `Makaronin: Budapest`
- `Punnany Massif: Pécs`

## Person entries

```md
### Artist Name
- aliases:
- groups:
- labels:
- region:
- notes:
```

### Akr
- aliases: 
- groups: Furakor, Káva
- labels: Garage
- region: Tatabánya
- notes: 

### Antal
- aliases: 
- groups: 
- labels: 
- region: 
- notes: duo with Day, folder `_magyar rap/Day, antal`.

### Artoscsaba
- aliases: 
- groups: Alakváltók
- labels: 
- region: 
- notes: 

### Authentic Beats
- aliases: 
- groups: 
- labels: AuthenticBeats Records
- region: 
- notes: producer.

### Awful
- aliases: 
- groups: 
- labels: RTM
- region: 
- notes: 

### AZA
- aliases: 
- groups: Killakikitt
- labels: SCBP
- region: Budapest
- notes: 

### Azahriah
- aliases: 
- groups: 
- labels: 
- region: Budapest
- notes: collabs with DESH and Young Fly.

### Bankos
- aliases: 
- groups: Az Idő Urai
- labels: Criminal
- region: Budapest
- notes: 

### Beton.Hofi
- aliases: 
- groups: 
- labels: 
- region: Budapest
- notes: 

### Bobafett
- aliases: 
- groups: 
- labels: 
- region: 
- notes: duo with Bobakrome, folder `_magyar rap/bobafett, bobakrome`.

### Bobakrome
- aliases: 
- groups: 
- labels: 
- region: 
- notes: duo with Bobafett, folder `_magyar rap/bobafett, bobakrome`.

### Bom
- aliases: 
- groups: DSP
- labels: Bloose Broavaz
- region: Budapest
- notes: 

### Bruno
- aliases: 
- groups: Bruno X Spacc
- labels: 
- region: 
- notes: 

### C2SH
- aliases: 
- groups: 
- labels: goldsoul
- region: 
- notes: 

### Chump_Yanz
- aliases: 
- groups: 
- labels: Bloose Broavaz
- region: 
- notes: 

### Curtis
- aliases: 
- groups: 
- labels: 
- region: Budapest
- notes: 

### Day
- aliases: 
- groups: 
- labels: 
- region: Eger
- notes: Sectah project. Duo with Antal, folder `_magyar rap/Day, antal`.

### Deego
- aliases: Diggieman
- groups: Barbárfivérek
- labels: Bloose Broavaz
- region: Győr
- notes: 

### DESH
- aliases: 
- groups: 
- labels: 
- region: Budapest
- notes: collabs with Azahriah and Young Fly.

### Dipa
- aliases: 
- groups: DSP
- labels: Bloose Broavaz
- region: Budapest
- notes: 

### Dirty
- aliases: 
- groups: 
- labels: Vicc Beatz
- region: 
- notes: 

### Drezzick
- aliases: 
- groups: Samurai Flow
- labels: Bloose Broavaz
- region: 
- notes: 

### Déó
- aliases: 
- groups: 
- labels: RTM
- region: 
- notes: 

### Eckü
- aliases: 
- groups: Gruppen Family, Hősök
- labels: Bloose Broavaz
- region: Veszprém
- notes: member of Hősök and Gruppen Family, NOT a Vicc Beatz artist.

### El Bago
- aliases: 
- groups: 
- labels: 
- region: Surány
- notes: 

### El Magico
- aliases: 
- groups: Káva
- labels: Garage
- region: Tatabánya
- notes: 

### eSGé
- aliases: 
- groups: Makaronin
- labels: 
- region: Budapest
- notes: 

### Essemm
- aliases: 
- groups: BeatMarket, Majmok Bolygója
- labels: Garage
- region: Kapuvár
- notes: 

### Fankadeli
- aliases: 
- groups: 
- labels: 
- region: Kecskemét
- notes: 

### Fiatal Veterán
- aliases: 
- groups: Teswér
- labels: 
- region: 
- notes: 

### Filo
- aliases: 
- groups: IFS
- labels: IFS
- region: Szeged
- notes: IFS member, Szeged. DIFFERENT PERSON from FILO in `_magyar trap` - never merge the two.

### FILO
- aliases: 
- groups: 
- labels: 
- region: 
- notes: `_magyar trap/FILO`. DIFFERENT PERSON from Filo of IFS - never merge the two.

### Frog
- aliases: 
- groups: 
- labels: Garage
- region: 
- notes: 

### Fullánk
- aliases: 
- groups: Jam Balaya
- labels: Vicc Beatz
- region: Győr
- notes: 

### Fura Csé
- aliases: 
- groups: Furakor, Káva
- labels: Garage
- region: Tatabánya
- notes: 

### G.w.M
- aliases: 
- groups: 
- labels: 
- region: Budapest
- notes: 

### Gaben
- aliases: 
- groups: BSW
- labels: 
- region: Somogy
- notes: 

### Giajenno
- aliases: 
- groups: AK26
- labels: RTM
- region: Surány
- notes: 

### Grasa
- aliases: 
- groups: 
- labels: 
- region: Budapest
- notes: 

### Hibrid
- aliases: 
- groups: Teswér
- labels: 
- region: 
- notes: 

### Hiro
- aliases: 
- groups: AK26
- labels: RTM
- region: Surány
- notes: 

### Illegalvoice
- aliases: 
- groups: New Fhészek
- labels: 
- region: 
- notes: producer and rapper. Files sit under `_magyar rap/Odupla`.

### K8
- aliases: Kolg8eight
- groups: 
- labels: 
- region: 
- notes: 

### KalashniKnow
- aliases: 
- groups: 
- labels: SCBP
- region: 
- notes: 

### Kamikaze
- aliases: 
- groups: 
- labels: RTM
- region: 
- notes: 

### Ketioz
- aliases: 
- groups: Egyenlők, Jam Balaya
- labels: Vicc Beatz
- region: Győr
- notes: 

### Kontroll
- aliases: 
- groups: 
- labels: Vicc Beatz
- region: 
- notes: 

### Kuli†King
- aliases: 
- groups: 
- labels: goldsoul
- region: 
- notes: 

### Lalipop
- aliases: 
- groups: 
- labels: Vicc Beatz
- region: 
- notes: 

### Landi
- aliases: 
- groups: 
- labels: Bloose Broavaz
- region: 
- notes: 

### LAzy
- aliases: 
- groups: 
- labels: 
- region: Pápa
- notes: 

### Majka
- aliases: 
- groups: 
- labels: 
- region: Ózd
- notes: 

### Marabela
- aliases: 
- groups: 
- labels: Vicc Beatz
- region: 
- notes: 

### Mentha
- aliases: 
- groups: Hősök
- labels: 
- region: Veszprém
- notes: 

### Mettyú
- aliases: 
- groups: BSW
- labels: 
- region: Somogy
- notes: 

### Miss Business
- aliases: 
- groups: 
- labels: Vicc Beatz
- region: 
- notes: 

### Mr. Missh
- aliases: 
- groups: 
- labels: 
- region: Almásfüzitő
- notes: 

### Mr.Busta
- aliases: 
- groups: 
- labels: RTM
- region: 
- notes: RTM label owner.

### Máté
- aliases: 
- groups: Punnany Massif
- labels: 
- region: Pécs
- notes: 

### night rainbow
- aliases: 
- groups: 
- labels: AuthenticBeats Records
- region: 
- notes: 

### Nomagróf
- aliases: 
- groups: Samurai Flow
- labels: Bloose Broavaz
- region: 
- notes: 

### Norba
- aliases: 
- groups: 
- labels: Criminal
- region: 
- notes: 

### Nos'chez
- aliases: 
- groups: Az Idő Urai, NKS
- labels: Criminal
- region: 
- notes: 

### Odupla
- aliases: 
- groups: Fhészek, New Fhészek
- labels: 
- region: 
- notes: Fhészek with The Steve, New Fhészek with Illegalvoice.

### P.G.
- aliases: 
- groups: 
- labels: goldsoul
- region: 
- notes: 

### P_s
- aliases: 
- groups: 
- labels: AuthenticBeats Records
- region: 
- notes: also written `3,14`. That alias cannot go in the aliases list - it contains a comma, which is the list separator.

### Phat
- aliases: 
- groups: Egyenlők, Rydu, Vészkijárat
- labels: Bloose Broavaz
- region: 
- notes: 

### PKO
- aliases: 
- groups: 
- labels: SCBP
- region: 
- notes: 

### Ra
- aliases: 
- groups: BeatMarket
- labels: Garage
- region: 
- notes: 

### Rambo
- aliases: 
- groups: Egyenlők, Jam Balaya
- labels: Vicc Beatz
- region: Győr
- notes: 

### redOne
- aliases: 
- groups: 
- labels: RTM
- region: 
- notes: 

### Rico
- aliases: 
- groups: 
- labels: goldsoul
- region: Gyöngyös
- notes: 

### Rizkay
- aliases: 
- groups: 
- labels: Bloose Broavaz
- region: 
- notes: beatmaker.

### Saiid
- aliases: 
- groups: Akkezdet Phiai
- labels: 
- region: Budapest
- notes: 

### San
- aliases: 
- groups: Dreamerz
- labels: Bloose Broavaz
- region: 
- notes: 

### Shuka
- aliases: 
- groups: 
- labels: SCBP
- region: 
- notes: 

### Siska Finuccsi
- aliases: 
- groups: Alakváltók, Egyenlők, Gruppen Family, Vészkijárat
- labels: Bloose Broavaz
- region: Tatabánya
- notes: 

### Smile of Hell
- aliases: 
- groups: IFS
- labels: IFS
- region: Szeged
- notes: 

### Sosa
- aliases: 
- groups: Makaronin
- labels: 
- region: Budapest
- notes: 

### Spacc
- aliases: 
- groups: Bruno X Spacc
- labels: 
- region: 
- notes: 

### Szalai
- aliases: 
- groups: ibbigang
- labels: 
- region: 
- notes: 

### Szimat
- aliases: 
- groups: Káva
- labels: Garage
- region: Tatabánya
- notes: 

### Süti
- aliases: 
- groups: Majmok Bolygója
- labels: Garage
- region: 
- notes: 

### Tactica
- aliases: 
- groups: 
- labels: SCBP
- region: 
- notes: 

### Tezsviir
- aliases: 
- groups: 
- labels: SCBP
- region: 
- notes: 

### The Steve
- aliases: Steve Antal
- groups: Fhészek
- labels: 
- region: 
- notes: 

### Tibbah
- aliases: 
- groups: Barbárfivérek
- labels: Bloose Broavaz
- region: Győr
- notes: 

### Tirpa
- aliases: 
- groups: Killakikitt
- labels: SCBP
- region: Budapest
- notes: 

### Tkyd
- aliases: 
- groups: Dreamerz, Rydu
- labels: Bloose Broavaz
- region: Pápa
- notes: 

### Turha
- aliases: Február
- groups: 
- labels: SCBP
- region: Tatabánya
- notes: 

### Valter
- aliases: 
- groups: ibbigang
- labels: 
- region: 
- notes: 

### Wolfie
- aliases: 
- groups: Punnany Massif
- labels: 
- region: Pécs
- notes: 

### Young Fly
- aliases: 
- groups: 
- labels: 
- region: 
- notes: collabs with DESH and Azahriah.

### Zenk
- aliases: 
- groups: Az Idő Urai, NKS
- labels: Criminal
- region: 
- notes: 

### Újonc Peti
- aliases: 
- groups: Akkezdet Phiai
- labels: 
- region: Budapest
- notes: 

## Folder-specific cleanup notes

Filename patterns seen in this area:

- `"02. Artist km. FeatArtist - Title.mp3"` - `km.` = közreműködik = featuring
- `"Artist km. Feat1, Feat2 - Title.mp3"`
- `"Artist - Title (by Producer).mp3"`
- `"01 - Artist - Title.mp3"`
- `közr.` is an alternative spelling of `km.`
- bitrate tags in folder names: `[320]`, `[192]`, `[128-256]`
- source tags: `[www.theraptunes.com]`, `(DatPiff.com)`
- many albums are double-nested: `Album [320]/Album [320]/files.mp3`

- **Hősök** - Eckü + Mentha plus two further members not yet identified.
- **Jereván Zoo** - Garage sub-project.
- **Sectah** - Day's solo project.
- **Weszélyes Elemek** - a Criminal act, treated as a single entity - do not split it into members.
