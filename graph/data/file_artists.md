# Per-file artists

Songs whose artist no rule can reach. The filename carries only a title and the folder is a
compilation, a mixtape series or an album whose artist has no other track in the collection —
so both the credit parser and the folder fallback come back empty.

Read by every area builder as the *last* fallback: a file listed here gets this artist only
when nothing else produced one. Nothing here overrides a working rule, so fixing a rule later
cannot silently conflict with this file.

Format, one per line:  `<collection-relative path> :: <artist>`

Attributed 2026-08-19 by reading each path with `claude -p`, then reviewed by hand. Only
high and medium confidence answers were kept; the 92 the reader called unknown are listed at
the bottom, commented out, so nobody spends time re-deriving them.

## Attributions

_magyar rap/_random/rimfarktush_-_infarktush/13. Infarktush km. Teoz, J-Boy.mp3 :: Rimfarktush
_magyar rap/_random/rimfarktush_-_infarktush/17. Utca.mp3 :: Rimfarktush
_rap/_usa other/Best Of   Too Short/The Ghetto.mp3 :: Too Short
_rap/_usa other/_random/013 - 2 Pistols ft. T-Pain _ Tay Dizm - She Got It      (™ Universal Republic).MP3 :: 2 Pistols
_rap/_usa other/_random/06 - Maejor Ali Bei Maejor Juicy J Justin Bieber - Lolly (DatPiff Exclusive).mp3 :: Maejor Ali   # medium confidence
_rap/_usa other/_random/100 Greatest Songs of Rap _ Hip Hop/100 - Ludacris - Southern Hospitality (2000).mp3 :: Ludacris
_rap/_usa other/_random/Alpha Dog Soundtrack - YouTube/alphadog soundtrack - tech n9ne - la la land (ft gina cassavetes).mp3 :: Tech N9ne
_rap/_usa other/_random/Awreeoh It_s my turn now.mp3 :: Awreeoh   # medium confidence
_rap/_usa other/_random/Babylon Warchild - The Gatekeepers (2012)/Babylon Warchild - The Gatekeepers (2012)/04 - The Towers Of Babylon Ft. Chief Kamachi _ Wordsworth.mp3 :: Babylon Warchild
_rap/_usa other/_random/Babylon Warchild - The Gatekeepers (2012)/Babylon Warchild - The Gatekeepers (2012)/13 - The Sacred Source Ft. Twin Perils.mp3 :: Babylon Warchild
_rap/_usa other/_random/M-Eighty _ Terminal 3 - The Academy 2 (2011)/M-Eighty _ Terminal 3 - The Academy 2 (2011)/06 - Rich Righteous Teachers Ft. Jadakiss, LA The Darkman, Sav Killz _ Billy Danze.mp3 :: M-Eighty & Terminal 3
_rap/_usa other/_random/M-Eighty _ Terminal 3 - The Academy 2 (2011)/M-Eighty _ Terminal 3 - The Academy 2 (2011)/13 - Body Down Ft. Styles P, Kojoe _ Jaecyn Bayne.mp3 :: M-Eighty & Terminal 3
_rap/_usa other/_random/NBA Live 2003 soundtrack - YouTube/NBA LIVE 2003 Soundtrack - Angie Martinez - If I C.mp3 :: Angie Martinez
_rap/_usa other/_random/NBA Live 2003 soundtrack - YouTube/NBA LIVE 2003 Soundtrack - Fabolous - It_s In The.mp3 :: Fabolous
_rap/_usa other/_random/NBA Live 2003 soundtrack - YouTube/NBA LIVE 2003 Soundtrack - Flipmode Squad (feat Bu.mp3 :: Flipmode Squad
_rap/_usa other/_random/NBA Live 2003 soundtrack - YouTube/NBA LIVE 2003 Soundtrack - Lyric - Young and Sexy.mp3 :: Lyric
_rap/_usa other/_random/NBA Live 2003 soundtrack - YouTube/NBA LIVE 2003 Soundtrack - Snoop Dogg - Get Live.mp3 :: Snoop Dogg
_rap/_usa other/_random/OfftheChain-Movie.com - Prodigal Sunn.mp3 :: Prodigal Sunn   # medium confidence
_rap/_usa other/_random/Simon Roofless - The Killing (2012)/Simon Roofless - The Killing (2012)/13 - I_m Done.mp3 :: Simon Roofless
_rap/_usa other/_random/Son Of Saturn - Thesis (2012)/Son Of Saturn - Thesis (2012)/12 - Daedalus Spoken.mp3 :: Son Of Saturn
_rap/_usa other/_random/Son Of Saturn - Thesis (2012)/Son Of Saturn - Thesis (2012)/13 - Again.mp3 :: Son Of Saturn
_rap/_usa other/_random/Son Of Saturn - Thesis (2012)/Son Of Saturn - Thesis (2012)/15 - Dont Take This Heaven.mp3 :: Son Of Saturn
_rap/_usa other/_random/Top 100 Old School Hip-Hop _ Rap Songs (1980-1991)/56. 5150 - Games People Play (1986).mp3 :: 5150   # medium confidence
_rap/_usa other/_random/VA-Underground_Babylon-You_Are_What_You_Know-(Mixtape)-2012-UB/VA-Underground_Babylon-You_Are_What_You_Know-(Mixtape)-2012-UB/10-Dr._Creep-In_a_Maze-(Prod._4th_Assassin)-UB.mp3 :: Dr. Creep   # medium confidence
_rap/_usa other/_random/VA-Underground_Babylon-You_Are_What_You_Know-(Mixtape)-2012-UB/VA-Underground_Babylon-You_Are_What_You_Know-(Mixtape)-2012-UB/25-Devasto-Representantes_da_Rua-UB.mp3 :: Devasto   # medium confidence
_rap/_usa other/_random/VA-Underground_Babylon-You_Are_What_You_Know-(Mixtape)-2012-UB/VA-Underground_Babylon-You_Are_What_You_Know-(Mixtape)-2012-UB/26-Killah_Priest-Brilliantaire-UB.mp3 :: Killah Priest
_rap/_usa other/_random/VA-Underground_Babylon-You_Are_What_You_Know-(Mixtape)-2012-UB/VA-Underground_Babylon-You_Are_What_You_Know-(Mixtape)-2012-UB/35-Sharon-Sono_Profundo-(Prod._FNDAF)-UB.mp3 :: Sharon   # medium confidence
_rap/_usa other/_random/VA-Underground_Babylon-You_Are_What_You_Know-(Mixtape)-2012-UB/VA-Underground_Babylon-You_Are_What_You_Know-(Mixtape)-2012-UB/38-Psych_Ward-Biophyzix-UB.mp3 :: Psych Ward   # medium confidence
_rap/_usa other/_random/Vendetta Kingz _ Anno Domini - V.K.A.D (2012)/Vendetta Kingz _ Anno Domini - V.K.A.D (2012)/02 - Dial V.mp3 :: Vendetta Kingz
_rap/_usa other/_random/Vendetta Kingz _ Anno Domini - V.K.A.D (2012)/Vendetta Kingz _ Anno Domini - V.K.A.D (2012)/12 - Eternalize.mp3 :: Vendetta Kingz
_rap/_usa other/_random/Vendetta Kingz _ Anno Domini - V.K.A.D (2012)/Vendetta Kingz _ Anno Domini - V.K.A.D (2012)/18 - Primal Urge.mp3 :: Vendetta Kingz
_rap/_usa other/_random/double life - YouTube/Double Life - Regiments.mp3 :: Regiments   # medium confidence
_rap/_usa other/_random/slum village Best Kept Secret/08 Get It Together (Madlib Remix).mp3 :: Slum Village
_rap/california/Dr.Dre Discography @320 (11 Albums)(RAP)(by dragan09)/Dr. Dre (1992) - The Chronic/05.Nuthin_ But A _G_ Thang.mp3 :: Dr. Dre
_rap/california/Dr.Dre Discography @320 (11 Albums)(RAP)(by dragan09)/Dr. Dre - Compton (Explicit) 2015 {MP3 Album}~{VBUc}/04 It_s All On Me (feat. Justus _ BJ the Chicago Kid).mp3 :: Dr. Dre
_rap/california/Dr.Dre Discography @320 (11 Albums)(RAP)(by dragan09)/Dr. Dre - Compton (Explicit) 2015 {MP3 Album}~{VBUc}/06 Darkside_Gone (feat. King Mez, Marsha Ambrosius _ Kendrick Lamar).mp3 :: Dr. Dre
_rap/california/Dr.Dre Discography @320 (11 Albums)(RAP)(by dragan09)/Dr. Dre - Compton (Explicit) 2015 {MP3 Album}~{VBUc}/08 Issues (feat. Ice Cube, Anderson .Paak _ Dem Jointz).mp3 :: Dr. Dre
_rap/california/Dr.Dre Discography @320 (11 Albums)(RAP)(by dragan09)/Dr. Dre - Compton (Explicit) 2015 {MP3 Album}~{VBUc}/09 Deep Water (feat. Kendrick Lamar, Justus _ Anderson .Paak).mp3 :: Dr. Dre
_rap/california/Dr.Dre Discography @320 (11 Albums)(RAP)(by dragan09)/Dr. Dre - Compton (Explicit) 2015 {MP3 Album}~{VBUc}/12 For the Love of Money (feat. Jill Scott, Jon Connor _ Anderson .Paak).mp3 :: Dr. Dre
_rap/california/Dr.Dre Discography @320 (11 Albums)(RAP)(by dragan09)/Dr. Dre - Compton (Explicit) 2015 {MP3 Album}~{VBUc}/15 Medicine Man (feat. Eminem, Candice Pillay _ Anderson .Paak).mp3 :: Dr. Dre
_rap/california/_random/Gangsta Rap   West Coast Hip Hop   G-Funk/Deep Cover (UNCENSORED) Dr. Dre ft. Snoop Dogg.mp3 :: Dr. Dre
_rap/california/_random/Gangsta Rap   West Coast Hip Hop   G-Funk/New Breed Of Hustlas City of Thugstas.mp3 :: New Breed Of Hustlas   # medium confidence
_rap/luisiana/_random/Mystikal - Prince Of The South (The Hits) [GangstaRapTalk.com][iTunes]/Mystikal - Prince Of The South (The Hits) [GangstaRapTalk.com][iTunes]/02 Shake Ya Ass (Ft. Pharrel Williams).mp3 :: Mystikal
_rap/memphis/Kingpin Skinny Pimp - 2000 RapDope Game/Don't Violate.mp3 :: Kingpin Skinny Pimp
_rap/new york/AZ/Aziatic/02 A-1 Performance 2.mp3 :: AZ
_rap/texas/_random/Lil O Stop Then Look feat Big Pokey, ESG, HAWK, Lil Keke, Mike D.mp3 :: Lil O   # medium confidence
_trap/_usa random/Best of EST Gee/XXL.mp3 :: EST Gee
_trap/_usa random/_random/Chance The Rapper - Acidrap/Chance_the_Rapper-Coloring_Book/Chance the Rapper - Coloring Book/07 - Mixtape (feat. Young Thug _ Lil Yachty).mp3 :: Chance The Rapper
_trap/_usa random/_random/HIPHOPTXL/Hip Hop TXL Vol 92 (Final)/52 Trippie Redd ft Rocket Da Goon x Lil Tracy - Limitless.mp3 :: Trippie Redd
_trap/_usa random/_random/HIPHOPTXL/Hip-Hop-TXL-Vol-87-HipHopTXL.com_/Hip Hop TXL Vol 87 [HipHopTXL.com]/61 Uncle Murda ft Young MA, Dios Moreno - THOT.mp3 :: Uncle Murda
_trap/_usa random/_random/HIPHOPTXL/TXL-96-MIXTAPE-HipHopTXL.com_/TXL 96 MIXTAPE (HipHopTXL.com)/41 Migos ft Cardi B and Nicki Minaj - Motor Sport.mp3 :: Migos
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL UK Vol 5 (DatPiff.com)/14 - J Spades Ft Mist Frisco M Darrg - Never Enough.mp3 :: J Spades
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 13 (DatPiff.com)/11 - YG ft Young Jeezy Rich Homie Quan - My Nigga (DatPiff Exclusive).mp3 :: YG
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 19 (DatPiff.com)/25 - PAPI (NORE) ft Lil Wayne Ja Rule Birdman - She Tried (Remix) (DatPiff Exclusive).mp3 :: NORE
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 20 (DatPiff.com)/01 - Big Sean ft Kendrick Lamar Jay Electronica - Control (DatPiff Exclusive).mp3 :: Big Sean
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 23 (DatPiff.com)/14 - Mike Will Made It ft Miley Cyrus Wiz Khalifa Juicy J - 23 (DatPiff Exclusive).mp3 :: Mike Will Made It
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 24 (DatPiff.com)/14 - August Alsina ft Trey Songz Chris Brown - I Luv This Shit (Remix) (DatPiff Exclusive).mp3 :: August Alsina
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 25 (DatPiff.com)/32 - Nipsey Hussle ft Rick Ross Cuzzy Capone - The Weather (DatPiff Exclusive).mp3 :: Nipsey Hussle
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 32 (DatPiff.com)/13 - Ty Dolla ign ft Wiz Khalifa DJ Mustard - Or Nah (DatPiff Exclusive).mp3 :: Ty Dolla $ign
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 33 (DatPiff.com)/05 - YG ft Lil Wayne Meek Mill Rich Homie Quan Nicki Minaj - My Nigga (Remix) (DatPiff Exclusive).mp3 :: YG
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 35 (DatPiff.com)/17 - Kid Ink ft 2 Chainz Juicy J Trey Songz Chris Brown - Show Me (Remix) (DatPiff Exclusive).mp3 :: Kid Ink
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 36 (DatPiff.com)/18 - Cap 1 ft OJ Da Juiceman 2 Chainz - Anywhere (DatPiff Exclusive).mp3 :: Cap 1
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 36 (DatPiff.com)/41 - Jadakiss ft Fabolous Bun B Rob Zoe Anthony King - Live For Today (DatPiff Exclusive).mp3 :: Jadakiss
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 39 (DatPiff.com)/27 - Sy Ari Da Kid ft Various Artists (TXL Artist) Tabius Tate - 300 Spartans (DatPiff Exclusive).mp3 :: Sy Ari Da Kid
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 43 (DatPiff.com)/02 - Mike Will Made It ft Future Lil Wayne Kendrick Lamar - Buy The World (DatPiff Exclusive).mp3 :: Mike Will Made It
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 43 (DatPiff.com)/17 - Akon ft Young Thug OG Boo Dirty - NASA (DatPiff Exclusive).mp3 :: Akon
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 43 (DatPiff.com)/23 - Ty Dolla ign ft The Weeknd Wiz Khalifa DJ Mustard - Or Nah (Official Remix) (DatPiff Exclusive).mp3 :: Ty Dolla $ign
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 43 (DatPiff.com)/26 - Maejor Ali ft Kid Ink Trey Songz - Me And My Team (DatPiff Exclusive).mp3 :: Maejor Ali
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 54 (DatPiff.com)/05 - Lil Wayne ft Christina Milian- Start A Fire (DatPiff Exclusive).mp3 :: Lil Wayne
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 60 (DatPiff.com)/09 - The Weeknd ft ScHoolboy Q Rick Ross - Often (Remix) (DatPiff Exclusive).mp3 :: The Weeknd
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 60 (DatPiff.com)/15 - Chance The Rapper ft The Social Expirement - No Better (DatPiff Exclusive).mp3 :: Chance The Rapper
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 70 (DatPiff.com)/03 - CurrenSy ft Lil Wayne August Alsina.mp3 :: Curren$y
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 73 (DatPiff.com)/27 - Kid Ink ft Vee Tha Rula Hardhead - I Been.mp3 :: Kid Ink
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 77 (DatPiff.com)/03 - Fred The Godson ft Joell Ortiz Vado - Ready To Start Pitchin.mp3 :: Fred The Godson
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 77 (DatPiff.com)/16 - Wiz Khalifa ft Ty Dolla Sign.mp3 :: Wiz Khalifa
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 80 (DatPiff.com)/17 - Nipsey Hussle ft Mike x Keys DJ Khalil - Ocean Views.mp3 :: Nipsey Hussle
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 81 (DatPiff.com)/25 - Fat Joe ft Jay Z Remy Ma Meek Mill Fabolous Jadakiss - All The Way Up (TXL Mix).mp3 :: Fat Joe
_trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 9 (DatPiff.com)/15 - TI ft Kendrick Lamar BoB Kris Stephens - Memories Back Then (DatPiff Exclusive).mp3 :: T.I.
_trap/_usa random/_random/Mix – Keith Ape - 잊지마 (It G Ma) (feat  JayAllDay, Loota, Okasian _ Kohh) [Official Video]/Keith Ape - 잊지마 (It G Ma) (feat. JayAllDay, Loota, Okasian _ Kohh) [Official Video].mp3 :: Keith Ape
_trap/_usa random/_random/Pro The Leader _ Dopestyle - Hip Hop Depression (2010)/Pro The Leader _ Dopestyle - Hip Hop Depression (2010)/07 - Despair Ft. Killah Priest.mp3 :: Pro The Leader & Dopestyle
_trap/_usa random/_random/Pro The Leader _ Dopestyle - Hip Hop Depression (2010)/Pro The Leader _ Dopestyle - Hip Hop Depression (2010)/09 - Get 1 Life.mp3 :: Pro The Leader & Dopestyle
_trap/_usa random/_random/Pro The Leader _ Dopestyle - Hip Hop Depression (2010)/Pro The Leader _ Dopestyle - Hip Hop Depression (2010)/13 - Waste No Time Ft. Atlantis Scrolls.mp3 :: Pro The Leader & Dopestyle
_trap/_usa random/_random/WSHH/Jacquees.mp3 :: Jacquees
_trap/_usa random/_random/Wale - The Gifted/Wale - Ambition [2011 Album]/11 Ambition (Feat. Meek Mill _ Rick Ross).mp3 :: Wale
_trap/_usa random/_random/bang101/Key Glock Orville Redenbacher (WSHH Exclusive - Official Audio).mp3 :: Key Glock
_trap/_usa random/lofihiphop/Sasori 蠍 - it_s not enough to say sorry (ft. importmedia).mp3 :: Sasori 蠍
_trap/_usa random/lofihiphop/Ｅｓｓｅｎｃｅ - why have we lost each other. (ft. Roiael).mp3 :: Ｅｓｓｅｎｃｅ
_trap/_usa random/lofihiphop/ＮＯＳＴＲＡＤＡＭＵＳ/Ｙｏｕ＇ｒｅ　Ｇｏｎｅ.mp3 :: ＮＯＳＴＲＡＤＡＭＵＳ
_trap/_usa random/random trap 15niggaz/Mateo Sun “BombFactory” (Prod. Ben Waid).mp3 :: Mateo Sun
_trap/atlanta/_random/2 Chainz/2 Chainz - Collegrove [iTunes]/04 - Gotta Lotta (feat. Lil Wayne).mp3 :: 2 Chainz
_trap/atlanta/_random/2 Chainz/2_Chainz-B.O.A.T.S_II-Metime-(Deluxe_Edition)/06 - Used 2.mp3 :: 2 Chainz
_trap/atlanta/_random/2 Chainz/2_Chainz-B.O.A.T.S_II-Metime-(Deluxe_Edition)/09 - U Da Realest.mp3 :: 2 Chainz
_trap/atlanta/_random/Shawt Bus Shawty Funny Rap Parody Cartoon Music Video @MikeRobBYOB.mp3 :: Mike Rob   # medium confidence
_trap/california/_random/yg/YG - My Crazy Life [Deluxe Edition] [2014] [EXPLICIT] [iTunes Plus] [M4V] + [M4A-256]-V3nom [GLT]/07 My Nigga (feat. Jeezy _ Rich Homi.mp3 :: YG
_trap/california/_random/yg/YG - My Crazy Life [Deluxe Edition] [2014] [EXPLICIT] [iTunes Plus] [M4V] + [M4A-256]-V3nom [GLT]/10 Who Do You Love_ (feat. Drake).mp3 :: YG
_trap/chicago/_random/Pound Cake By Otf Nunu Shot Directed By THE FILM GOD 2014.mp3 :: OTF Nunu   # medium confidence
_trap/detroit/42 dugg/42 Dugg - FREE DEM BOYZ (Full Album)/We Know.mp3 :: 42 Dugg
_trap/florida/_random/Yung Simmie 🔥💯/Yung Simmie - Fake Nikkas 2 (Prod. DjSmokey).mp3 :: Yung Simmie
_trap/memphis/yo gotti/Moneybagg Yo, GloRilla & CMG The Label - Gangsta Art 2/CMG The Label, 42 Dugg – Bae (Official Audio).mp3 :: 42 Dugg   # medium confidence
_trap/_usa random/Pnb rock playlist ❤️/28. I Like Girls (feat. Lil Skies).mp3 :: PnB Rock   # second pass: Folder named 'Pnb rock playlist' indicates artis
_trap/_usa random/𝑃𝑅𝐸𝑆𝐸𝑁𝑇𝐼𝑁𝐺 𝐶𝐼𝑇𝑌 𝐺𝐼𝑅𝐿𝑆/Act Up.mp3 :: City Girls   # second pass: Folder name 'PRESENTING CITY GIRLS' suggests art

## Not attributable

# _rap/memphis/All Tracks - DJ Squeeky/Do My Thang Pop My Wip.mp3   (unsure: Folder says 'All Tracks - DJ Squeeky' which could mean DJ-curate)

Third audit round, 2026-08-19:

# _rap/_usa other/_random/Fat Joe Remy Ma French Montana Ry SO Valid - Cookin.mp3   (wrong: This is a Fat Joe & Remy Ma collaboration as a duo; proposing on)
# _rap/_usa other/_random/Fat Joe Remy Ma JAY Z French Montana InfaRed - All The Way Up (Remix).mp3   (wrong: Fat Joe & Remy Ma are billed as co-primary artists on this track)
# _rap/new york/_random/15   D I T C   Tribute.mp3   (wrong: A 'Tribute' track is typically BY other artists honoring D.I.T.C)

A second, stricter audit on 2026-08-19 removed these. A DJ who compiled the tape,
a label executive, or a various-artists compilation is not the recording artist:

# _rap/_usa other/_random/M-Eighty _ Terminal 3 - The Academy 2 (2011)/M-Eighty _ Terminal 3 - The Academy 2 (2011)/15 - Paperwork Ft. Keith Murray, Sean Price _ Big Lou.mp3   (wrong: Folder shows 'M-Eighty & Terminal 3' as the album artists, but pro)
# _rap/_usa other/_random/Underground Hip Hop Mega Pack/Seven_s Travels/19 Always Coming Back Home To You.mp3   (unsure: Path shows 'Seven's Travels' folder under 'Underground Hip Hop Meg)
# _rap/_usa other/_random/VA-Underground_Babylon-You_Are_What_You_Know-(Mixtape)-2012-UB/VA-Underground_Babylon-You_Are_What_You_Know-(Mixtape)-2012-UB/07-Apakalypse___Son_of_Saturn-Future_Teacherz-UB.mp3   (wrong: Filename shows 'Apakalypse___Son_of_Saturn' - this is a collaborat)
# _rap/_usa other/_random/VA-Underground_Babylon-You_Are_What_You_Know-(Mixtape)-2012-UB/VA-Underground_Babylon-You_Are_What_You_Know-(Mixtape)-2012-UB/34-Imperial_Skillz_Empera___Gamblez-Behind_Deaths_Door-UB.mp3   (wrong: Filename shows 'Imperial_Skillz_Empera___Gamblez' - collaboration.)
# _rap/_usa other/_random/Vinz Vega _ True Grit - Requiem From The Darkness (2010)/Vinz Vega _ True Grit - Requiem From The Darkness (2010)/12 - Smoke In Tha Lungz Ft. Dirrty Peddlaz.mp3   (wrong: Folder shows 'Vinz Vega & True Grit - Requiem From The Darkness' -)
# _rap/texas/_random/swisha house-drank up in my cup.mp3   (wrong: Swisha House is a label/collective (DJ Michael Watts), not the per)
# _trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 32 (DatPiff.com)/14 - Ty Dolla ign ft Trey Songz French Montana - Paranoid (Remix) (DatPiff Exclusive).mp3   (unsure: YouTube matched ASH ISLAND's 'Paranoid Remix' - completely differe)
# _trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 33 (DatPiff.com)/11 - DJ Kay Slay ft 50 Cent Fat Joe - Free Again (DatPiff Exclusive).mp3   (wrong: DJ Kay Slay is a DJ/compiler, not the recording artist. 50 Cent an)
# _trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 35 (DatPiff.com)/09 - The Weeknd Ty Dolla ign Wiz Khalifa - Or Nah (Weeknd Remix) (DatPiff Exclusive).mp3   (wrong: The Weeknd made a remix but 'Or Nah' is Ty Dolla $ign's song - Ty$)
# _trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 35 (DatPiff.com)/15 - Kanye West TI Beyonce Jay Z - Drunk In Love (Hip Hop TXL Remix Edit) (DatPiff Exclusive).mp3   (wrong: 'Drunk In Love' is Beyoncé's song, Kanye and others are on the rem)
# _trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 41 (DatPiff.com)/28 - Dame Dash ft Jim Jones Smoke DZA - Dont Get Scared (DatPiff Exclusive).mp3   (wrong: Dame Dash is a label executive/mogul (Roc-A-Fella), not a recordin)
# _trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 50 (DatPiff.com)/41 - - Jadakiss ft Fabolous Bun B Rob Zoe Anthony King - Live For Today (DatPiff Exclusive).mp3   (wrong: YouTube shows 'Live For Today' by Sean C featuring Jadakiss and ot)
# _trap/_usa random/_random/bang101/BROKE MY WRIST LIL PUMP X SMOKEPURPP (PROD BY RONNYJLI$TENUP).mp3   (unsure: Track is 'Lil Pump X Smokepurpp' - both artists are co-primaries, )
# _trap/memphis/yo gotti/Yo Gotti & CMG The Label - Gangsta Art (FULL ALBUM)/Hold Me Down.mp3   (wrong: Folder is 'Yo Gotti & CMG The Label - Gangsta Art' - a label compi)

Removed 2026-08-19 after an audit against each file's YouTube match. Most are
compilation folders — a DJ album, a label sampler or a mixtape series names the
compiler, not the performer:

# _magyar rap/_random/rimfarktush_-_infarktush/16. Otthon édes otthon.mp3   (wrong: YouTube shows Tirpa feat. NKS as the artist, not Rimfarktush. The fold)
# _magyar rap/_random/rimfarktush_-_infarktush/18. Hova tartunk.mp3   (wrong: YouTube shows USEME as the artist. Rimfarktush folder appears to conta)
# _rap/_usa other/_random/Babylon Warchild - The Gatekeepers (2012)/Babylon Warchild - The Gatekeepers (2012)/03 - The System.mp3   (wrong: YouTube match shows WonkyWilla, Homemade Spaceship, Def3 - completely )
# _rap/_usa other/_random/Funk Master Flex _ Big Kap - The Tunnel (1999)/Funk Master Flex _ Big Kap - The Tunnel (1999)/02 - Flex _ Biggie Tupac Live Freestyle.mp3   (wrong: Funk Master Flex & Big Kap - The Tunnel is a DJ compilation album feat)
# _rap/_usa other/_random/Funk Master Flex _ Big Kap - The Tunnel (1999)/Funk Master Flex _ Big Kap - The Tunnel (1999)/07 - Prodigy _ Kool G Rap _ QBG.mp3   (wrong: DJ compilation album. The filename itself shows 'Prodigy & Kool G Rap')
# _rap/_usa other/_random/VA-Underground_Babylon-You_Are_What_You_Know-(Mixtape)-2012-UB/VA-Underground_Babylon-You_Are_What_You_Know-(Mixtape)-2012-UB/03-Premeditação-Meu_Lugar-(Prod._Nítido_Beats)-UB.mp3   (wrong: VA (Various Artists) folder - Underground Babylon mixtape is a compila)
# _rap/_usa other/_random/VA-Underground_Babylon-You_Are_What_You_Know-(Mixtape)-2012-UB/VA-Underground_Babylon-You_Are_What_You_Know-(Mixtape)-2012-UB/15-Antraz-Desabafo_do_Mundo-(Prod._Antraz)-UB.mp3   (wrong: Same VA compilation mixtape. YouTube shows Mr.Grisalho. Attribution fr)
# _trap/_usa random/Best of EST Gee/EVERY CHANCE I GET.mp3   (wrong: YouTube clearly shows this is DJ Khaled's song featuring Lil Baby & Li)
# _trap/_usa random/_random/HIPHOPTXL/Hip-Hop-TXL-Vol-86-HipHopTXL.com_/Hip Hop TXL Vol 86 (HipHopTXL.com)/46 Peter Jackson x Maino ft Michael Mazze - Oh Lord (TXL Feature).mp3   (wrong: HIPHOPTXL is a mixtape/compilation series (Various Artists). Peter Jac)
# _trap/_usa random/_random/HIPHOPTXL/TXL-96-MIXTAPE-HipHopTXL.com_/TXL 96 MIXTAPE (HipHopTXL.com)/49 Roy Woods Ft Lil Yachty _ Swae Lee - Afterparty.mp3   (wrong: HIPHOPTXL compilation. YouTube shows Tech N9ne Collabos with completel)
# _trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 5 (DatPiff.com)/08 - Tabius Tate ft Calico Jones Mucho Dinero - Nite Life (TXL Premier) (DatPiff Exclusive).mp3   (unsure: HIPHOPTXL is a compilation. Tabius Tate is marked as the artist in fil)
# _trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 73 (DatPiff.com)/41 - Tabius Tate (TXL Artist) ft Dane Jalee Stack 5 Castle Calhoun - Hold On (TXL Feature).mp3   (unsure: Same HIPHOPTXL compilation issue. Tabius Tate marked in filename but Y)
# _trap/_usa random/_random/Mix – Kur - Lets Keep It A Bean ( Official Video ) By Rick Nyce/Yerkys (Full Music Video) @Lilcaycay_.mp3   (unsure: Folder is a playlist/mix. YouTube shows 'popstarr' not Lil Caycay. Can)
# _trap/_usa random/lofihiphop/ＮＯＳＴＲＡＤＡＭＵＳ/ＢＵＲＤＥＮ.mp3   (unsure: ＮＯＳＴＲＡＤＡＭＵＳ is a lofi artist folder. YouTube shows Ashley Singh - like)
# _trap/_usa random/lofihiphop/ＮＯＳＴＲＡＤＡＭＵＳ/ＩＭＡＧＩＮＥ.mp3   (unsure: Same lofi folder. YouTube shows Neuro4typical - likely wrong match. Ca)
# _trap/_usa random/lofihiphop/ＮＯＳＴＲＡＤＡＭＵＳ/ＩＳＯＬＡＴＥＤ.mp3   (unsure: Same lofi folder. YouTube shows Dayymein - generic title, likely wrong)
# _trap/_usa random/lofihiphop/ＮＯＳＴＲＡＤＡＭＵＳ/ＬＯＯＫＩＮＧ　ＦＯＲ　ＳＯＭＥＴＨＩＮＧ.mp3   (unsure: Same lofi folder. YouTube shows NEIKED - likely wrong match for this g)
# _trap/_usa random/lofihiphop/ＮＯＳＴＲＡＤＡＭＵＳ/ＮＯＳＴＡＬＧＩＣ.mp3   (unsure: Same lofi folder. YouTube shows Vin Jay, Bingx, Masetti - generic titl)
# _trap/_usa random/lofihiphop/ＮＯＳＴＲＡＤＡＭＵＳ/Ｗａｔｃｈ　ｉｔ　ｆｌｙ.mp3   (unsure: Same lofi folder. YouTube shows American Teleport - cannot verify if f)
# _trap/memphis/yo gotti/Yo Gotti & CMG The Label - Gangsta Art (FULL ALBUM)/SOON.mp3   (unsure: Yo Gotti & CMG The Label is a label compilation album (Gangsta Art). Y)

The path genuinely does not say who recorded these. Left unattributed on purpose —
an invented artist is worse than an honest blank.

# _rap/_usa other/_random/01 All Say 1.mp3
# _rap/_usa other/_random/I_m Da Man.mp3
# _rap/_usa other/_random/Ode to New York (Official Video).mp3
# _rap/_usa other/_random/Top 100 R_B/Back At One.mp3
# _rap/_usa other/_random/Top 100 R_B/First We Pray.mp3
# _rap/_usa other/_random/Top 100 R_B/Full Moon.mp3
# _rap/_usa other/_random/Top 100 R_B/I_m Real (Remix).mp3
# _rap/_usa other/_random/Top 100 R_B/Never Again.mp3
# _rap/_usa other/_random/Top 100 R_B/Never Thought.mp3
# _rap/_usa other/_random/Top 100 R_B/Read Your Mind.mp3
# _rap/_usa other/_random/Top 100 R_B/Ride Wit U.mp3
# _rap/_usa other/_random/Top 100 R_B/Right Here [Departed].mp3
# _rap/_usa other/_random/Top 100 R_B/Southside (Feat. Ashanti).mp3
# _rap/_usa other/_random/Top 100 R_B/The Boy Is Mine.mp3
# _rap/_usa other/_random/Top 100 R_B/You Are Not Alone.mp3
# _rap/_usa other/_random/Top 100 R_B/all_my_life.mp3
# _rap/_usa other/_random/Top 100 R_B/how_you_gonna_act_like_that.mp3
# _rap/_usa other/_random/Top 100 R_B/playas_only_(feat_the_game).mp3
# _rap/_usa other/_random/Top 100 R_B/rise_and_fall_(featuring_sting).mp3
# _rap/_usa other/_random/Top 100 R_B/satisfy_you_(feat_r_kelly)-tatsh_int.mp3
# _rap/_usa other/_random/Top 100 R_B/walking_away.mp3
# _rap/california/_random/Bay Area Rap Classics 90_s/I_m a Player (Street Version).mp3
# _rap/california/_random/Bay Area Rap Classics 90_s/Let_s Ride (Bonus Track).mp3
# _rap/california/_random/Bay Area Rap Classics 90_s/Welcome To the Ghetto.mp3
# _rap/california/_random/Gangsta Rap   West Coast Hip Hop   G-Funk/Fuck Wit Dre Day (feat. DR. Dre, Snoop Dogg).mp3
# _rap/california/_random/Gangsta Rap   West Coast Hip Hop   G-Funk/Pump Yo Brake.mp3
# _rap/memphis/MEMPHIS RAP Top 50 all-time/Lock Em in da Trunk (feat. DJ Zirk).mp3
# _rap/new york/_random/Epilogue.mp3
# _rap/new york/_random/Got Ya Back.mp3
# _rap/new york/_random/Next Level (Nyte Time Mix).mp3
# _rap/texas/_random/Attention.mp3
# _rap/texas/_random/Big Moe Mann (Screwed).mp3
# _rap/texas/_random/Get Up Off Me (feat. U.G.K.).mp3
# _rap/texas/_random/I'm Throwed (feat. Jermaine Dupri).mp3
# _rap/texas/_random/Recognize A Playa.mp3
# _rap/texas/_random/Ride 4s.mp3
# _rap/texas/_random/Ridin On 4's (feat. Slim Thug).mp3
# _rap/texas/_random/Sex Faces.mp3
# _rap/texas/_random/Swang {S.U.C. Remix} Feat. Trae, Big Pokey, Pimp C, Big H.A.W.K., Bun B & Fat Pat (Music Video).mp3
# _rap/texas/_random/Thug.mp3
# _rap/texas/_random/Wood Wheel.mp3
# _trap/_usa random/Get It Up.mp3
# _trap/_usa random/Maybach.mp3
# _trap/_usa random/Quickie.mp3
# _trap/_usa random/_random/Ep - Paper chase (full song)/Me Vs Me.mp3
# _trap/_usa random/_random/Ep - Paper chase (full song)/No Sucker.mp3
# _trap/_usa random/_random/HIPHOPTXL/DJ_Reddy_Rell-Hip_Hop_TXL_Vol._66/04 - 3500.mp3
# _trap/_usa random/_random/HIPHOPTXL/DJ_Reddy_Rell-Hip_Hop_TXL_Vol._66/19 - Poppin (TXL Remix).mp3
# _trap/_usa random/_random/HIPHOPTXL/DJ_Reddy_Rell-Hip_Hop_TXL_Vol._66/32 - 4 A Minute.mp3
# _trap/_usa random/_random/HIPHOPTXL/DJ_Reddy_Rell-Hip_Hop_TXL_Vol._66/47 - Dont Panic.mp3
# _trap/_usa random/_random/HIPHOPTXL/DJ_Reddy_Rell-Hip_Hop_TXL_Vol._68/26 - Back Up.mp3
# _trap/_usa random/_random/HIPHOPTXL/DJ_Reddy_Rell-Hip_Hop_TXL_Vol._68/39 - For Rich Or Poor.mp3
# _trap/_usa random/_random/HIPHOPTXL/DJ_Reddy_Rell-Hip_Hop_TXL_Vol._68/40 - Famous.mp3
# _trap/_usa random/_random/HIPHOPTXL/DJ_Reddy_Rell-Hip_Hop_TXL_Vol._68/43 - My Love.mp3
# _trap/_usa random/_random/HIPHOPTXL/DJ_Reddy_Rell-Hip_Hop_TXL_Vol._68/48 - On Go.mp3
# _trap/_usa random/_random/HIPHOPTXL/DJ_Reddy_Rell-Hip_Hop_TXL_Vol._68/51 - We High.mp3
# _trap/_usa random/_random/HIPHOPTXL/DJ_Reddy_Rell-Hip_Hop_TXL_Vol._75/04 - Out My Face.mp3
# _trap/_usa random/_random/HIPHOPTXL/DJ_Reddy_Rell-Hip_Hop_TXL_Vol._75/15 - Nu Gambino.mp3
# _trap/_usa random/_random/HIPHOPTXL/DJ_Reddy_Rell-Hip_Hop_TXL_Vol._75/47 - 7 Figures.mp3
# _trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 48/02 - Don_t Shoot.mp3
# _trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 48/17 - Driving Ms Daisy.mp3
# _trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 48/30 - Ballin.mp3
# _trap/_usa random/_random/HIPHOPTXL/Various Artists - Hip Hop TXL Vol 77 (DatPiff.com)/28 - S16.mp3
# _trap/_usa random/_random/We Bout Dat Life Vol  2 - YouTube/Fell Out.mp3
# _trap/_usa random/_random/We Bout Dat Life Vol  2 - YouTube/Wat l Like.mp3
# _trap/_usa random/_random/bang101/02 Shit Remix (Ft Rich The Kid).mp3
# _trap/_usa random/_random/bang101/24 Already.mp3
# _trap/_usa random/_random/bang101/Bird Is The Word.mp3
# _trap/_usa random/_random/bang101/Boss.mp3
# _trap/_usa random/_random/bang101/Fingers Blue (feat Travis Scott).mp3
# _trap/_usa random/_random/bang101/Fr Fr (feat Lil Skies).mp3
# _trap/_usa random/_random/bang101/Gatecode (Prod Lord Casso).mp3
# _trap/_usa random/_random/bang101/H2O (feat XXXTENTACION).mp3
# _trap/_usa random/_random/bang101/Hot.mp3
# _trap/_usa random/_random/bang101/Intro Fuck 12.mp3
# _trap/_usa random/_random/bang101/Molly.mp3
# _trap/_usa random/_random/bang101/Pump 93 Prod By [kayGW Beats].mp3
# _trap/_usa random/_random/bang101/Russian Cream.mp3
# _trap/_usa random/_random/crank/CARTIZ.mp3
# _trap/_usa random/_random/iLLmixtapes.com/06 Fuck B_tches , Get Money.mp3
# _trap/_usa random/_random/volume 1/What You Want.mp3
# _trap/_usa random/lofihiphop/ＥＭＰＴＹ.mp3
# _trap/memphis/yo gotti/Moneybagg Yo, GloRilla & CMG The Label - Gangsta Art 2/50 50.mp3
# _trap/memphis/yo gotti/Moneybagg Yo, GloRilla & CMG The Label - Gangsta Art 2/Cha Cha Cha.mp3
# _trap/memphis/yo gotti/Moneybagg Yo, GloRilla & CMG The Label - Gangsta Art 2/Justify (Freestyle).mp3
# _trap/memphis/yo gotti/Moneybagg Yo, GloRilla & CMG The Label - Gangsta Art 2/Log Off.mp3
# _trap/memphis/yo gotti/Moneybagg Yo, GloRilla & CMG The Label - Gangsta Art 2/One Time.mp3
# _trap/memphis/yo gotti/Moneybagg Yo, GloRilla & CMG The Label - Gangsta Art 2/Overstood.mp3
# _trap/memphis/yo gotti/Yo Gotti & CMG The Label - Gangsta Art (FULL ALBUM)/(FREE) Shiva X Rhove Type Beat - RESIDENCE.mp3
# _trap/memphis/yo gotti/Yo Gotti & CMG The Label - Gangsta Art (FULL ALBUM)/(FREE) Simba La Rue X Keta Type Beat - SINNER.mp3
