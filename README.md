# MusicSCAN for World of Warcraft: Forever

A standalone jukebox for Blizzard music included with World of Warcraft: Forever.
**Less configuring. More listening.**

Developed by **SCAN | Kilobytes Development**. Based on
[MusicSCAN](https://github.com/Scandallisk/MusicSCAN) 0.7.1 BETA.
This repository maintains the Forever target separately from Retail.

## Current test build

**0.7.1-forever-alpha.2**, targeting Forever **1.60.1.70888**, interface **16001**.
This is an alpha test build; a public beta release has not been published here.

- 200 retained Original World of Warcraft music entries.
- 370 Forever-folder music candidates, including filename associations for Hyjal,
  Riverglades, Summit of Eternity, Sunnyglade and other locations/shared themes.
- Eleven Retail expansion categories removed from this target.
- Search, expansion browsing, Favorites, Play/Stop, movable/resizable window and minimap launcher.
- Loading-screen recovery restarts the active track; login and reload remain idle.
- No bundled audio, streaming, dependencies on other addons, or duration-based timers.

The owner confirmed alpha.1 runs and tested Original WoW music plays; expansion music
tested there did not. Alpha.2's new music IDs are **not yet audibly verified**.
Filename-derived labels are provisional and do not establish complete zone coverage.
The installed-client root manifest and zone-music table joins have not been validated.
Report silent/mislabeled entries with displayed title, location, FileDataID and client build.

## Install

Copy the repository's **MusicSCAN/** folder into your Forever client's
**Interface/AddOns/** directory, so MusicSCAN.toc is directly inside MusicSCAN/.
Do not install the entire repository as the addon folder. Start/restart the client,
enable MusicSCAN, then use `/msc`, `/musicscan`, or the minimap button.
Select a track and press Play. Stop releases the override to normal zone music.
The star targets the selected track; selection alone does not switch playback.
Preserve your WTF/SavedVariables files during upgrades. Missing-catalog Favorite IDs
are retained but hidden; an unavailable selection falls back to an original track.

## Development

Python 3.9+ is used for tooling; the addon itself is Lua and has no Python dependency.

```sh
python -m pip install -r tests/requirements.txt
python tests/run_lua.py
python tools/build_release.py
```

Tests mock the native WoW frame/audio environment under Lua 5.1 and 5.4. They check
catalog identity, category scope, Favorites persistence, selection fallback, bounded
rows, audio errors, and loading recovery/cancellation. They do not verify audible music.
The packager creates an installable eight-file ZIP and checksum in ignored `dist/`.

See [catalog provenance](catalog/CATALOG-SOURCE.json),
[catalog regeneration](docs/CATALOG.md), [client test plan](docs/CLIENT-TEST.md),
and [validation record](docs/VALIDATION.txt).

## License

**All Rights Reserved.** Personal installation and local modification are permitted
as described in [LICENSE.txt](LICENSE.txt). Public source availability does not grant
an open-source license. Blizzard music and third-party metadata retain their own rights.

https://kilobytes.dev/musicscan/
