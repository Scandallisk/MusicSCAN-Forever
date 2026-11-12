# Catalog maintenance

`MusicSCAN/Database.lua` is generated metadata; no audio is shipped.
`catalog/original-wow-records.txt` freezes the 200 unchanged Original WoW records
from MusicSCAN 0.7.1 BETA. Do not change their selection keys or FileDataIDs casually.
`catalog/FOREVER-CATALOG.csv` lists all 415 current records; excluded cue records
and per-location counts are in `catalog/CATALOG-SOURCE.json`.

The generator accepts only the exact `sound.csv` URL and SHA256 pinned in
`tools/catalog-source.json`. Download that immutable URL separately, then run:

```sh
python tools/build_catalog.py --source /path/to/sound.csv
python tests/run_lua.py
python -m unittest discover -s tests -p "test_*.py"
```

Generation is offline and updates Database.lua, FOREVER-CATALOG.csv and catalog counts.
No client archive scan, table join, music download or listening verification is performed.
Refreshing inputs or filename-location rules requires review. Do not replace the pinned
source with the latest file silently. Review excluded cues and preserve stable identities.
Unmapped themes remain Other Zone Music; location labels are filename associations.

## Duplicate audit in alpha.3

The 570-entry alpha.2 catalog contained 155 metadata-equivalent original/Forever pairs.
136 match conservatively normalized filenames/titles; 19 use reviewed spelling/numbering
rules in `tools/catalog-duplicate-overrides.json`. All 17 repeated Ahn'Qiraj entries match.
`catalog/DUPLICATE-AUDIT.csv` records every pair, both source paths and the reason.

Keep the original ID for an overlap because original playback has user confirmation.
Move all 200 original records into the Forever category, and retain the 215 additional
Forever candidates: 415 rows in one category. Original keys, titles and FileDataIDs remain
unchanged. The frozen input retains its historical category for provenance only.

Generated FileIDAliases/TrackKeyAliases resolve removed duplicate IDs/keys to canonical
original rows. Saved alias Favorite IDs are preserved; Favorites queries deduplicate by
canonical key, and removing a Favorite clears both IDs. No wholesale SavedVariables migration.

This is a metadata audit, not audio fingerprinting. Matching names may refer to different
recordings; only one representative is shown. Original variants remain accessible through
the canonical original row; new-file aliases are recorded for review. Distinct day/night,
intro/zone, lettered and numbered variants are not merged by broad title similarity.

Valid saved Favorite IDs survive removal from this target. Do not delete user SavedVariables.
Forever-folder IDs that reference older location names are distinct from the removed
Retail expansion records. Shared installation storage alone is not proof that an asset
belongs to the Forever client. Compare the specific build manifest before claiming availability.
