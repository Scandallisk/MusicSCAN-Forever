# MusicSCAN 0.7.1-forever-beta.1

Public beta candidate for World of Warcraft: Forever 1.60.1.70888 (interface 16001).

Browse 415 entries in one World of Warcraft: Forever category: all 200 original
music IDs plus 215 additional Forever-file candidates. Alpha.3 consolidates 155
metadata-equivalent original/Forever pairs, including 17 repeated Ahn'Qiraj entries.
Original IDs remain canonical for those pairs; saved alternate IDs still resolve.
Removed the eleven Retail expansion categories from this build. All retained tracks now appear under World of Warcraft: Forever, including the
original tracks. Metadata matching is not proof of identical audio recordings.
This is a metadata-based test catalog, not a fully verified soundtrack or complete zone list.

Use /msc or /musicscan to open the player. Select a track, then press Play.
Selection alone does not play. Stop returns control to the game's normal music.
Star favorites the selected track. Closing the window keeps music playing.
Loading recovery restarts the active track; login and /reload never autoplay.
Drag the title bar to move, the lower-right grip to resize, and the minimap icon to reposition.
/msc reset restores window/minimap geometry while preserving Favorites and selection.

Your local test confirmed that alpha.1 runs and Original WoW music plays;
expansion-category music tested there did not play. New Forever IDs still need listening tests.
If a track is silent or mislabeled, report its title, zone and tooltip FileDataID.
The Playing label records an accepted request and cannot independently verify audible output.

Preferences use MusicSCANDB. Consolidated duplicate IDs share one Favorite row;
removing that Favorite clears both IDs. Unrelated missing-catalog Favorite IDs are
retained but hidden. No SavedVariables file is deleted.
An unavailable saved selection falls back to a retained original track. No bundled audio,
external streaming, dependencies, timers for repetition, progress bar, or seeking.

SCAN | Kilobytes Development — https://kilobytes.dev/musicscan/

Beta 1 retains the alpha.3 playback/catalog behavior. The AddOns list title is
MusicSCAN Forever; the runtime folder remains MusicSCAN. Additional Forever candidates
still await listening verification. Report title, location, FileDataID and client build at
https://github.com/Scandallisk/MusicSCAN-Forever/issues
All Rights Reserved; see LICENSE.txt. No bundled Blizzard audio.
