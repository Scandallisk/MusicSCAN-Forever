# Music catalog provenance and limits

Metadata only. Blizzard audio is provided by the user's installed game, not this addon.
All music rights remain with their respective owners; see LICENSE.txt for addon terms.

Original catalog: 200 records from the Original World of Warcraft category in MusicSCAN 0.7.1 BETA.
Alpha.3 changes only their category to World of Warcraft: Forever. Their stable keys,
titles, source metadata and audio FileDataIDs remain unchanged.

Forever filename metadata: wowdev/wow-listfile parts/sound.csv
- Immutable source: https://raw.githubusercontent.com/wowdev/wow-listfile/deeca4ac550d28d49f38be5248367a0b2eceb840/parts/sound.csv
- Metadata revision: deeca4ac550d28d49f38be5248367a0b2eceb840
- Source SHA256: 0ce7afe81799443daa809b6287dc5cbddd11c78e06fa22e0830a05e2958c6a83
- Retrieved: 2026-11-12
- Selection: Sound/Music/Forever/ audio files, excluding explicit event/character intros,
  Moment/Dance cues, Darkmoon Faire and Zalazane's Fall, and test/voice/cinematic cues.
- 370 eligible candidates before duplicate consolidation; 17 cues excluded from 387
  Forever-folder records. Alpha.3 consolidates 155 of those 370 with canonical originals,
  leaving 215 additional candidates alongside the 200 originals (415 browser rows).
- The 155 overlaps are metadata identities, not audio fingerprints: 136 normalized
  filename/title matches and 19 reviewed naming aliases. Original IDs remain canonical;
  generated runtime aliases preserve old duplicate selections and Favorite IDs.
- The source repository records all pairs in catalog/DUPLICATE-AUDIT.csv.

Only audio FileDataIDs are passed to PlaySoundFile on Master, never SoundKit IDs.
Friendly titles and locations are filename associations, not official soundtrack titles
or verified zone-usage mappings. Unmapped themes appear under Other Zone Music.
Some Forever filenames reference locations also named in Retail expansions; those are
distinct Forever-folder IDs, not restoration of the removed Retail expansion categories.

This catalog has not been checked against the installed client's root manifest or zone-music
table joins, and the new IDs have not been audibly verified. Filename availability does not
prove client availability, zone use, or complete new-zone coverage. Report silent/mislabeled
entries by title, location and FileDataID. No audio files are downloaded or packaged.

## 0.8 theme views

Six reviewed zone/filename rule sets in tools/theme-rules.json generate Themes.lua
from catalog/FOREVER-CATALOG.csv. Membership reasons are in catalog/THEME-AUDIT.csv.
Views do not add music records or verify playback, and may overlap. Unknown zones
remain accessible in All Music. The underlying catalog and aliases are unchanged.
