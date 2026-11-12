# MusicSCAN Forever test history

## 0.7.1-forever-alpha.3
- Audit and consolidate 155 metadata-equivalent original/Forever pairs (136 normalized
  matches and 19 reviewed spelling/numbering aliases), including 17 Ahn'Qiraj duplicates.
- Keep original IDs as canonical and move all 200 original records into Forever.
- One World of Warcraft: Forever category: 415 rows (200 original + 215 additional).
- Preserve saved duplicate selections/Favorites through runtime aliases; both IDs
  produce one Favorite, and unfavoriting clears both. Unknown valid Favorite IDs survive.
- Add a complete pair audit and regressions for all 155 alias mappings and variant safety.
- This is metadata consolidation; identical audio recordings have not been established.

## 0.7.1-forever-alpha.2
- Retain 200 Original WoW entries with unchanged keys and FileDataIDs.
- Add 370 Forever-file music candidates with filename-derived labels.
- Exclude 17 event/character or nonbackground cues pending separate review.
- Remove 5,293 original Retail expansion entries from this target's catalog.
- Preserve valid Favorite IDs; no playback or SavedVariables schema changes.
- Set a retained Original WoW default instead of the removed Magnificent Desolation selection.

## 0.7.1-forever-alpha.1
- Initial local Forever player compatibility test; interface 16001 and Monk-color fallback.
- User confirmed the player works and Original WoW music plays; expansion music tested did not.

Based on the MusicSCAN 0.7.1 BETA runtime. Retail checkout remains unchanged.
