# MusicSCAN for World of Warcraft: Forever

A standalone jukebox for Blizzard music included with World of Warcraft: Forever.
**Less configuring. More listening.**

Developed by **SCAN | Kilobytes Development**. Based on
[MusicSCAN](https://github.com/Scandallisk/MusicSCAN) 0.7.1 BETA.
This repository maintains the Forever target separately from Retail.

## Public beta release

**0.7.1-forever-beta.1**, targeting Forever **1.60.1.70888**, interface **16001**.
Published November 12, 2026 as a GitHub beta prerelease.
[Download the installable ZIP](https://github.com/Scandallisk/MusicSCAN-Forever/releases/download/v0.7.1-forever-beta.1/MusicSCAN-0.7.1-forever-beta.1.zip) · [Release notes](https://github.com/Scandallisk/MusicSCAN-Forever/releases/tag/v0.7.1-forever-beta.1)
The source repository is public; the addon remains All Rights Reserved.
See the release notes for installation, feedback instructions and known limits.

- One **World of Warcraft: Forever** category with **415 catalog entries**.
- All 200 original music IDs retained and moved into the Forever category.
- 215 additional Forever-folder candidates, including filename associations for Hyjal,
  Riverglades, Summit of Eternity, Sunnyglade and other locations/shared themes.
- 155 metadata-equivalent original/Forever pairs consolidated; 17 repeated Ahn'Qiraj entries removed.
- Eleven Retail expansion categories remain absent from this target.
- Search, expansion browsing, Favorites, Play/Stop, movable/resizable window and minimap launcher.
- Loading-screen recovery restarts the active track; login and reload remain idle.
- No bundled audio, streaming, dependencies on other addons, or duration-based timers.

The owner confirmed alpha.1 runs and tested Original WoW music plays; expansion music
tested there did not. Alpha.2 introduced the Forever candidate set; alpha.3 consolidates its
metadata duplicates. Additional Forever IDs are **not yet audibly verified**.
Filename-derived labels are provisional and do not establish complete zone coverage.
The installed-client root manifest and zone-music table joins have not been validated.
Report silent/mislabeled entries with displayed title, location, FileDataID and client build.

## Install

For a packaged build, extract the installable ZIP and copy its **MusicSCAN/** folder
into your Forever client's
**Interface/AddOns/** directory, so MusicSCAN.toc is directly inside MusicSCAN/.
The folder name must stay **MusicSCAN**, even though the AddOns list title is
**MusicSCAN Forever**. Do not install the entire source repository as the addon folder.
This package is specifically for Forever; retain Retail's separate package in its own client. Start/restart the client,
enable MusicSCAN, then use `/msc`, `/musicscan`, or the minimap button.
Select a track and press Play. Stop releases the override to normal zone music.
The star targets the selected track; selection alone does not switch playback.
Preserve your WTF/SavedVariables files during upgrades. Missing-catalog Favorite IDs
are retained but hidden; an unavailable selection falls back to an original track.
Selections and Favorites saved under consolidated duplicate IDs still resolve to the
retained original row. Both IDs produce only one Favorite; removing that Favorite clears both.

## Development

Python 3.9+ is used for tooling; the addon itself is Lua and has no Python dependency.

```sh
python -m pip install -r tests/requirements.txt
python tests/run_lua.py
python -m unittest discover -s tests -p "test_*.py"
python tools/build_release.py
```

Tests mock the native WoW frame/audio environment under Lua 5.1 and 5.4. They check
catalog identity, category scope, Favorites persistence, selection fallback, bounded
rows, audio errors, and loading recovery/cancellation. They do not verify audible music.
The duplicate audit checks normalized filenames/titles plus reviewed naming aliases;
it does not prove identical audio recordings. Day/night and numbered/lettered variations
remain separate. See [all 155 consolidated pairs](catalog/DUPLICATE-AUDIT.csv).
The packager creates an installable eight-file ZIP and checksum in ignored `dist/`.

See [catalog provenance](catalog/CATALOG-SOURCE.json),
[catalog regeneration](docs/CATALOG.md), [client test plan](docs/CLIENT-TEST.md),
and [validation record](docs/VALIDATION.txt).

## License

**All Rights Reserved.** Personal installation and local modification are permitted
as described in [LICENSE.txt](LICENSE.txt). Public source availability does not grant
an open-source license. Blizzard music and third-party metadata retain their own rights.

https://kilobytes.dev/musicscan/
