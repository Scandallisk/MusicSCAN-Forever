# MusicSCAN Forever 0.8.0 BETA1

**Less configuring. More listening.**

Version **0.8.0-forever-beta.1** · Forever **1.60.1.70888** · Interface **16001**

## What's new

- Split-screen library sidebar and track pane with independent scrolling.
- Six themed playlists: Cities **43**, Forests **44**, Taverns **42**, PvP **16**,
  Dungeons **30**, Raids **57**.
- All **415** deduplicated catalog records and **155** saved-track aliases retained.
- Play captures the current ordered library/search results as a fixed queue.
- Automatic Next and the Next button advance through the queue and wrap at the end.
- Repeat ON repeats the active track; OFF automatically advances. Next always advances.
- Browsing, search, highlighted selection and Favorite edits leave the queue unchanged.
- Repeat/loading recovery retain an independently highlighted selection. Favorites
  target that highlighted row. Login/reload stay idle; closing the window keeps playback.

## Audio behavior — please read

Selected music follows **Master Volume**. MusicSCAN temporarily sets only **Music
Volume** to zero to suppress normal zone music, retaining its previous value.
Stop, failure, logout/reload and loading suspension restore it; loading recovery
reacquires suppression. Other sliders are unchanged. Music-slider changes made
during playback are respected on Stop. Raising Music Volume during playback can
make zone music audible again. Use **/msc restore** to stop and retry pending
restoration. After a hard crash, restore Music Volume manually if necessary.

A sound-handle watcher runs only during playback. No guessed durations. Handles
never observed playing time out after 30 seconds; failed files stop the queue
instead of endlessly skipping. Handle termination cannot distinguish every
interruption from a natural ending. Required audio APIs are checked before playback.
No audio is bundled/downloaded, no addon dependencies and no addon network requests.

## Install / upgrade

1. Stop MusicSCAN, then fully exit Forever. Back up your existing addon folder.
2. Download **MusicSCAN-0.8.0-forever-beta.1.zip**, the installable release asset,
   from [GitHub Releases](https://github.com/Scandallisk/MusicSCAN-Forever/releases/tag/v0.8.0-forever-beta.1)
   or the [CurseForge Files tab](https://www.curseforge.com/wow/addons/musicscan-forever/files/all)
   when the beta is approved. CurseForge users may need the Beta files filter.
3. Replace **MusicSCAN/** under your Forever client's **Interface/AddOns/**,
   so MusicSCAN.toc is directly inside MusicSCAN, without an extra nested folder.
   Keep the folder name MusicSCAN and preserve WTF/SavedVariables.
4. Fully restart Forever to discover the two new modules. Enable **MusicSCAN Forever**.
5. Open **/msc**, **/musicscan**, or the minimap button. Use **/msc reset** for the
   new 760x560 default window (minimum 620x460); valid saved layout remains supported.

Choose a library and track, then Play. A selected track outside the current
library/search queues that selection alone. Next always advances. Repeat affects
the active track; Favorites affect the highlighted row. Stop restores zone music.
Rollback: fully exit Forever, move the beta folder aside and restore your backup;
preserve SavedVariables. This package targets Forever; Retail has its own package.

| Command (/msc or /musicscan) | Action |
| --- | --- |
| no argument | Open/close player |
| play | Play highlighted track and capture queue |
| stop | Stop and restore normal zone music |
| next | Advance/wrap the queue |
| repeat | Toggle repeating active track |
| status | Show playback and queue status |
| restore | Stop and retry pending Music Volume restoration |
| reset | Restore default window/minimap layout |
| help | Show commands |

## Testing and catalog limits

The owner confirmed **Next, Repeat and themed playlists work in Forever** on this
local build and authorized this beta publication. Retail's POC3 had separately
confirmed automatic progression, zone suppression and Stop restoration.
Mocked Lua 5.1/5.4 tests (with and without a Monk class color) pass for the 415-row
catalog, all 155 alias migrations, unique theme membership, bounded native UI row
reuse, frozen/search queues, Next/Repeat, loading cancellation, missing APIs,
startup timeout, errors, restoration retry and logout. Four Python catalog tests
also pass. These are not exhaustive listening, travel or client-build tests; the
latest Forever report did not separately confirm every audio/transition scenario.

All 200 original records and 215 additional Forever-folder candidates are retained.
Additional IDs have not all been audibly verified. Zone/title associations remain
provisional; no complete zone coverage or client-manifest/zone-table validation is
claimed. Themes are reviewed zone/filename associations rather than exhaustive
official playlists. Unknown locations remain in All Music. Overlapping themes
reference existing canonical records rather than adding duplicate catalog entries.

## Feedback and rights

[Report issues](https://github.com/Scandallisk/MusicSCAN-Forever/issues) with track
title, location, FileDataID, client build, exact Lua error and reproduction steps.
For queue issues include library/search/Repeat state; for recovery include travel
route. Do not attach account details or full SavedVariables files.

SCAN | Kilobytes Development · https://kilobytes.dev/musicscan/
All Rights Reserved; personal installation/local modification per LICENSE.txt.
Blizzard audio and third-party metadata retain their rights. Public source does
not grant an open-source license.
