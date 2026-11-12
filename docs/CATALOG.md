# Catalog maintenance

`MusicSCAN/Database.lua` is generated metadata; no audio is shipped.
`catalog/original-wow-records.txt` freezes the 200 unchanged Original WoW records
from MusicSCAN 0.7.1 BETA. Do not change their selection keys or FileDataIDs casually.
`catalog/FOREVER-CATALOG.csv` lists the 370 new candidate records; excluded cue records
and per-location counts are in `catalog/CATALOG-SOURCE.json`.

The generator accepts only the exact `sound.csv` URL and SHA256 pinned in
`tools/catalog-source.json`. Download that immutable URL separately, then run:

```sh
python tools/build_catalog.py --source /path/to/sound.csv
python tests/run_lua.py
```

Generation is offline and updates Database.lua, FOREVER-CATALOG.csv and catalog counts.
No client archive scan, table join, music download or listening verification is performed.
Refreshing inputs or filename-location rules requires review. Do not replace the pinned
source with the latest file silently. Review excluded cues and preserve stable identities.
Unmapped themes remain Other Zone Music; location labels are filename associations.

Valid saved Favorite IDs survive removal from this target. Do not delete user SavedVariables.
Forever-folder IDs that reference older location names are distinct from the removed
Retail expansion records. Shared installation storage alone is not proof that an asset
belongs to the Forever client. Compare the specific build manifest before claiming availability.
