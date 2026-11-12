# MusicSCAN Forever 0.7.1 Beta 1

First public beta candidate for **World of Warcraft: Forever**.
Version: **0.7.1-forever-beta.1** · Target client: **1.60.1.70888** · Interface: **16001**

## What it does

Play Blizzard's built-in music while exploring World of Warcraft: Forever.
Browse one Forever category, search tracks and locations, save Favorites, and use
explicit Play/Stop controls. The compact native window moves and resizes, and a
draggable minimap launcher provides quick access. Loading-screen recovery restarts
the active track from the beginning; login and reload never start playback automatically.

**Less configuring. More listening.**

## Catalog and changes

- **415 entries**: 200 retained original music IDs and 215 additional Forever-file candidates.
- All tracks appear in **World of Warcraft: Forever**, followed by Favorites.
- 155 metadata-equivalent original/Forever pairs consolidated, including 17 Ahn'Qiraj pairs.
- Saved selections and Favorites using a consolidated ID resolve to the retained original row.
- Distinct numbered, lettered, day/night and intro/zone variations remain separate.
- The eleven unavailable Retail expansion categories remain excluded from this target.
- AddOns-list title identifies the package as MusicSCAN Forever; runtime folder stays MusicSCAN.
- This beta promotion changes versioning and documentation, not playback or catalog membership.

## Install or update

1. Download **MusicSCAN-0.7.1-forever-beta.1.zip** (the installable ZIP).
2. Exit WoW. Extract the ZIP into your Forever client's `Interface/AddOns/` directory.
3. Confirm `Interface/AddOns/MusicSCAN/MusicSCAN.toc` exists directly at that path.
4. Start Forever, enable **MusicSCAN Forever**, then enter `/msc` or `/musicscan`.
5. Select a track, then press Play. Press Stop to return control to normal zone music.

When upgrading, replace the existing MusicSCAN addon folder while preserving your
WTF/SavedVariables files. Do not delete MusicSCANDB or install a second folder alongside
MusicSCAN: preferences use the same addon identity. This package targets Forever only.
GitHub's automatic “Source code” archives are developer snapshots, not the installable ZIP.

Commands: `/msc` toggles the window; `/msc play`, `/msc stop`, `/msc help`, and
`/msc reset` are also available. Reset preserves Favorites and selection.
Select alone does not switch the active music. Closing the window does not stop playback.

## Test status and known limits

- The owner confirmed that the Forever player runs and tested original music plays.
- The 215 additional Forever candidates **still need in-game listening verification**.
- Lua 5.1/5.4 mocked regression tests cover Favorites, alias preservation, search,
  viewport behavior, playback failures and loading-screen recovery/cancellation.
- Catalog tests check all original identities, reviewed duplicate mappings and variant safety.
- These automated checks do not verify audible output or guarantee client compatibility.
- Names/locations derive from community filenames and are provisional. Complete new-zone
  coverage and installed-client manifest/zone-music-table membership have not been established.
- Duplicate consolidation uses metadata identities, not audio fingerprints; different IDs
  could be different encodes or arrangements. Original IDs are retained for those pairs.
- A Playing label records an accepted request, not independent confirmation of audible sound.
- Recovery restarts a file; there is no exact-position resume, seeking, duration/progress display,
  play-once guarantee or addon-managed repetition timer.

## Feedback

Report silent tracks, wrong locations, duplicates or Lua errors through
[GitHub Issues](https://github.com/Scandallisk/MusicSCAN-Forever/issues).
Include the client build, displayed title/location, tooltip **FileDataID**, exact Lua error,
and reproduction steps. For recovery issues, include the travel route and whether Stop/Play
was pressed during the transition. Do not attach account details or your full SavedVariables file.

## Integrity and rights

`SHA256SUMS.txt` contains the installable ZIP's checksum. The ZIP contains eight files
under one MusicSCAN folder, with no developer tools, personal settings or bundled music.

**SCAN | Kilobytes Development** — [kilobytes.dev/musicscan](https://kilobytes.dev/musicscan/#forever)
**All Rights Reserved.** Personal installation/local modification per LICENSE.txt;
public source availability does not grant an open-source license. Blizzard audio and
third-party metadata retain their respective rights. No addon dependencies or audio downloads.
