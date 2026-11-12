# Music catalog provenance and limits

Metadata only. Blizzard audio is provided by the user's installed game, not this addon.
All music rights remain with their respective owners; see LICENSE.txt for addon terms.

Original catalog: 200 records copied byte-for-byte from the Original World of Warcraft
category in the MusicSCAN 0.7.1 BETA database. Their stable keys and audio FileDataIDs remain unchanged.

Forever filename metadata: wowdev/wow-listfile parts/sound.csv
- Immutable source: https://raw.githubusercontent.com/wowdev/wow-listfile/deeca4ac550d28d49f38be5248367a0b2eceb840/parts/sound.csv
- Metadata revision: deeca4ac550d28d49f38be5248367a0b2eceb840
- Source SHA256: 0ce7afe81799443daa809b6287dc5cbddd11c78e06fa22e0830a05e2958c6a83
- Retrieved: 2026-11-12
- Selection: Sound/Music/Forever/ audio files, excluding explicit event/character intros,
  Moment/Dance cues, Darkmoon Faire and Zalazane's Fall, and test/voice/cinematic cues.
- 370 included; 17 excluded, out of 387 Forever-folder records.

Only audio FileDataIDs are passed to PlayMusic, never SoundKit IDs.
Friendly titles and locations are filename associations, not official soundtrack titles
or verified zone-usage mappings. Unmapped themes appear under Other Zone Music.
Some Forever filenames reference locations also named in Retail expansions; those are
distinct Forever-folder IDs, not restoration of the removed Retail expansion categories.

This alpha has not been checked against the installed client's root manifest or zone-music
table joins, and the new IDs have not been audibly verified. Filename availability does not
prove client availability, zone use, or complete new-zone coverage. Report silent/mislabeled
entries by title, location and FileDataID. No audio files are downloaded or packaged.
