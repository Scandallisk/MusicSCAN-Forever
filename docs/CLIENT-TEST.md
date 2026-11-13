# MusicSCAN Forever 0.8.0 BETA1 — client test plan

Version: 0.8.0-forever-beta.1. Target: Forever 1.60.1.70888, interface 16001.
The owner confirmed Next, Repeat and themed playlists work in Forever.
The following checklist supports wider beta testing; remaining scenarios are not assumed verified.

## Changes

- Retail's tested sound-handle playback engine, automatic Next and Repeat toggle.
- Split library sidebar/track pane, independently scrolling.
- All Music, Favorites, six themed playlists and the single Forever category.
- Cities 43; Forests 44; Taverns 42; PvP 16; Dungeons 30; Raids 57.
- All 415 records and all 155 canonical-key/FileDataID aliases retained unchanged.
- Play captures the current ordered library/search results. Browsing and Favorite
  edits leave that queue unchanged. Next advances and wraps even with Repeat ON.
- Repeat ON repeats the active track; OFF automatically advances through the queue.
- Repeat/loading recovery retain an independently highlighted selection. Favorites
  target the highlighted row. Login/reload stay idle; closing the window keeps playback.

## Audio behavior

Selected music follows **Master Volume**. MusicSCAN temporarily sets only **Music
Volume** to zero to suppress normal zone music, retaining its previous value.
Stop, failure, logout/reload and loading suspension restore it; loading recovery
reacquires suppression. Music-slider changes made during playback are respected
on Stop. Raising Music Volume during playback can make zone music audible again.
Use **/msc restore** to stop and retry pending restoration. After a hard crash,
restore Music Volume manually in Audio settings if necessary.

Uses PlaySoundFile FileDataIDs on Master, C_Sound.IsPlaying and a 0.2s watcher only
during playback. No guessed durations. Never-observed handles time out after 30s;
failed files stop the queue rather than endlessly skipping. Handle termination
cannot distinguish every interruption from a natural ending. Missing required
audio APIs produce a safe diagnostic. The latest Forever report confirms Next,
Repeat and themes; broader audio/loading validation remains on this checklist.

## Start testing

1. Fully restart Forever after the addon files are installed; new Lua modules need
   a restart to be discovered. Enable **MusicSCAN Forever** in the AddOns list.
2. Open **/msc**. Use **/msc reset** for the new 760x560 default layout (minimum
   620x460); saved valid geometry/Favorites/selections are retained.
3. Select **Cities**, clear search, highlight **Darnassus Introduction**, then Play.
   Confirm only the chosen music is audible and Master Volume controls it.
4. With Repeat OFF, listen for **Darnassus Walking (Variation 1)** after the intro.
   Click Next to advance immediately; Repeat ON should repeat the active track.
   Next must still advance with Repeat ON. To test wrap quickly, star two tracks,
   use Favorites, then Play and press Next through both tracks.
5. Stop must restore your previous Music Volume and zone music. Browse/search or
   edit Favorites while playing; the active captured queue should remain unchanged.
6. Play A, highlight B, then cross a loading screen. A should restart, B stay
   highlighted, and there should be no skip caused by loading. Stop during recovery
   must cancel it. Login/reload must not autoplay.
7. Try the six theme views and Favorites, resizing, minimap dragging and scrolling.
   New Forever-folder entries remain candidates: report silent/mislabeled files.

Commands: /msc (or /musicscan), play, stop, next, repeat, status, restore, reset, help.
If the highlighted track is outside the active library/search, Play queues only that
selection. Library headings/folds do not remove records from a captured queue.

## Catalog and validation limits

Database.lua is byte-identical to the existing Forever beta, including duplicate
aliases. No Retail expansion catalog was imported. Theme views reference canonical
keys; a record may appear in several views without creating duplicate records.
Reviewed zone/filename associations are not exhaustive official playlists. Dalaran,
Hyjal and other filename associations retain the existing catalog's provisional
status. Generic/unknown locations remain in All Music. Gnomeragon is classified
under Dungeons rather than inferred to be a major city from its source folder.

The existing 200 original tracks and 215 additional Forever-folder candidates are
retained. Additional IDs have not all been audibly verified; no new claim of full
zone coverage or a client-manifest/zone-table join is made.

Mocked Lua 5.1/5.4 integration tests, with/without a Monk color, cover the unchanged
catalog, all 155 alias migrations, theme uniqueness, bounded native row reuse,
frozen/search queues, Next/Repeat, loading cancellation, missing audio APIs, startup
timeout, errors, pending-volume retry and logout. Four Python catalog-audit tests
also pass. Mocks do not validate native rendering or audible playback; the owner separately
confirmed Next, Repeat and themed playlists in-game.

## Installation / rollback

Install only MusicSCAN/ inside the Forever client's Interface/AddOns/ so that
MusicSCAN.toc is directly inside it. Preserve WTF/SavedVariables and the folder
name MusicSCAN. Retail is a separate installation. No audio is bundled or downloaded.

For rollback: fully exit Forever, move the beta folder aside and restore your
previous addon backup. Preserve SavedVariables. Restore Music Volume manually if
needed after a crash. See RELEASE-NOTES.md for the current public beta details.
