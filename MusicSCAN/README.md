# MusicSCAN 0.7.1-forever-alpha.2

Local test build for World of Warcraft: Forever 1.60.1.70888 (interface 16001).

Browse 200 Original World of Warcraft tracks and 370 Forever-file music entries.
Removed the eleven Retail expansion categories from this build. Forever-file variants
remain under World of Warcraft: Forever even when their filenames reference older locations.
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

Preferences use MusicSCANDB. Missing-catalog Favorite IDs are retained but hidden.
An unavailable saved selection falls back to a retained original track. No bundled audio,
external streaming, dependencies, timers for repetition, progress bar, or seeking.

SCAN | Kilobytes Development — https://kilobytes.dev/musicscan/
