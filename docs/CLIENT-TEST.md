# Forever Beta 1 client tests

Target: 1.60.1.70888. These checks require a player; mocks cannot establish audible output.

1. Open `/msc`; check 0.7.1-forever-beta.1 in the footer and one Forever category (415) plus Favorites.
2. Play a retained original track, then Hyjal General A (8158670), Riverglades General A
   (8158714), Summit of Eternity A (8158682), and Sunnyglade A (8173719).
3. Confirm audible identity. Highlight B while A plays: A must continue. Play switches to B.
4. Stop returns control to normal zone music. Closing/reopening the window preserves playback.
5. Favorite a new track; reload. Favorite/selection/geometry persist and playback stays idle.
6. With active A and highlighted B, cross a loading screen: A restarts. Stop during the
   transition/delay prevents restart. Explicit Play must win over pending recovery.
7. Check resize, minimap drag, search and Favorites at minimum window size.

Record route, client build, displayed title, FileDataID, result and exact Lua errors.
An accepted PlayMusic request or Playing label is not evidence of audible output.
Alpha.1 was confirmed working with original music; alpha.2's new IDs remain pending.

8. Search Ahn'Qiraj: expect 18 entries (17 retained original tracks and one additional
   Ruins Triangle Room entry), with no second copy under an Original WoW category.
9. A selected/Favorited alpha.2 duplicate such as music-8176626 should resolve to
   music-53261 after reload. Favoriting both old and new IDs shows one Favorite.
   Remove it, reload, and verify it stays removed. Favorites for unrelated removed
   expansion IDs stay stored but hidden.
