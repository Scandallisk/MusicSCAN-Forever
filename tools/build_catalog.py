"""Regenerate only catalog metadata from an explicit, hash-pinned source CSV.

python tools/build_catalog.py --source /path/to/sound.csv
Downloads and refreshing upstream data are deliberately separate operations.
"""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADDON = ROOT / 'MusicSCAN'
LOCATIONS = {
    'Hyjal_General': 'Hyjal', 'HyjalExtWalk': 'Hyjal',
    'Mournings_Rest': "Mourning's Rest", 'Summit_of_Eternity': 'Summit of Eternity',
    'Bolderok': 'Bolderok', 'Eastwind_Shore': 'Eastwind Shore',
    'Farholde_Keep': 'Farholde Keep', 'Riverglades_General': 'Riverglades',
    'Rogmar_Outpost': 'Rogmar Outpost', 'Twilights_Shroud': "Twilight's Shroud",
    'Wheelers_Grange': "Wheeler's Grange", 'Gustberry_Lowlands': 'Gustberry Lowlands',
    'Shadowgale_Forest': 'Shadowgale Forest', 'Shendar_Hub': 'Shendar',
    'Shrine_of_Akir': 'Shrine of Akir', 'Thendal_Village': 'Thendal Village',
    'Cradle_of_Tranquility': 'Cradle of Tranquility', 'Felblood_Scar': 'Felblood Scar',
    'Sunnyglade': 'Sunnyglade', 'Valanaar': 'Valanaar', 'Shrine_of_Aviana': 'Shrine of Aviana',
    'AhnQiraj': "Ahn'Qiraj", 'Darnasssus': 'Darnassus', 'Darnassus': 'Darnassus',
    'Ironforge': 'Ironforge', 'Stormwind': 'Stormwind', 'Orgrimmar': 'Orgrimmar',
    'Undercity': 'Undercity', 'Thunder_Bluff': 'Thunder Bluff', 'Warrior_Terrace': 'Darnassus',
    'Gnomeragon': 'Gnomeregan', 'Naxxramas': 'Naxxramas',
    'Dalaran': 'Dalaran', 'Sholazar': 'Sholazar (Filename Association)',
    'Terrokar_Bone_Wastes': 'Bone Wastes (Filename Association)',
    'Nerubian_Nest': 'Nerubian Nest', 'Silken_Path': 'Silken Path',
    'Weavers_Lair': "Weaver's Lair", 'Stranglethorn': 'Stranglethorn Vale',
    'Daegun': 'Daegun', 'Elderwild': 'Elderwild', 'Freehold': 'Freehold',
    'Malornes_Retreat': "Malorne's Retreat", 'Naga_Incursion': 'Naga Incursion',
    'Riplash': 'Riplash', 'Tainted_Foothills': 'Tainted Foothills',
}

def lua_string(value):
    return json.dumps(value, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path)
    args = parser.parse_args()
    global PINNED
    PINNED = args.source
    source = json.loads((ROOT / 'tools/catalog-source.json').read_text(encoding='utf-8'))
    actual_hash = hashlib.sha256(PINNED.read_bytes()).hexdigest()
    if actual_hash != source['sourceSHA256']:
        raise SystemExit('Source SHA256 differs from pinned metadata; review before refreshing inputs.')
    originals = (ROOT / 'catalog/original-wow-records.txt').read_text(encoding='utf-8').splitlines()
    assert len(originals) == 200
    original_keys = [re.search(r'key="([^"]+)"', line)[1] for line in originals]
    original_ids = [int(re.search(r'fileDataID=(\d+)', line)[1]) for line in originals]
    records, excluded = [], []
    for line in PINNED.read_text(encoding='utf-8-sig').splitlines():
        if ';' not in line:
            continue
        file_id, filename = line.split(';', 1)
        if not filename.lower().startswith('sound/music/forever/'):
            continue
        # Leave event/character cues out rather than assuming every music file is zone background music.
        if re.search(r'(?i)(test|unused|beta|cinematic|scene|voice|stinger|jingle|_moment|_dance|darkmoon_faire|zalazanes_fall|skyborne.*intro)', filename):
            excluded.append({'fileDataID': int(file_id), 'sourceFilename': filename,
                             'reason': 'event-character-intro-or-nonbackground-cue'})
            continue
        stem = Path(filename).stem
        assert re.match(r'^MUS_C(?:60)?_', stem), filename
        label = re.sub(r'^MUS_C(?:60)?_', '', stem)
        zone = next((v for k, v in sorted(LOCATIONS.items(), key=lambda item: -len(item[0]))
                     if label == k or label.startswith(k + '_')), 'Other Zone Music')
        if label.startswith('Dungeons_'):
            zone = 'Dungeons: ' + re.sub(r'_[A-Z]$', '', label[len('Dungeons_'):]).replace('_', ' ')
        title = label.replace('AhnQiraj', "Ahn'Qiraj").replace('Darnasssus', 'Darnassus')
        title = title.replace('HyjalExtWalk', 'Hyjal Exterior Walking').replace('_', ' ')
        title = re.sub(r'\bIntro\b', 'Introduction', title)
        records.append(dict(key=f'music-{file_id}', title=title, zone=zone,
                            expansion='World of Warcraft: Forever', fileDataID=int(file_id),
                            sourceFilename=filename, playbackVerified=False,
                            mappingSource='forever-filename-association'))
    ids = original_ids + [r['fileDataID'] for r in records]
    keys = original_keys + [r['key'] for r in records]
    assert len(ids) == len(set(ids)) and len(keys) == len(set(keys))
    records.sort(key=lambda r: (r['zone'].lower(), r['title'].lower(), r['fileDataID']))
    text = ('-- MusicSCAN Forever alpha: metadata only; no bundled audio.\n'
            '-- Filename-derived labels are provisional; see SOURCES.md.\nlocal _, ns = ...\n\n'
            'ns.ExpansionOrder = { ["Original World of Warcraft"] = 1, ["World of Warcraft: Forever"] = 2 }\n\nns.Catalog = {\n')
    text += '\n'.join(originals) + '\n'
    for record in records:
        fields = []
        for key, value in record.items():
            encoded = 'false' if value is False else str(value) if isinstance(value, int) else lua_string(value)
            fields.append(f'{key}={encoded}')
        text += '    {' + ', '.join(fields) + '},\n'
    text += '}\n\nns.DEFAULT_TRACK_KEY = ' + lua_string(original_keys[0]) + '\n'
    (ADDON / 'Database.lua').write_text(text, encoding='utf-8')
    with (ROOT / 'catalog/FOREVER-CATALOG.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    manifest_path = ROOT / 'catalog/CATALOG-SOURCE.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    manifest.update(originalCount=len(originals), foreverCount=len(records), total=len(ids),
                    excludedCount=len(excluded), excluded=excluded,
                    zoneCounts=dict(sorted(Counter(r['zone'] for r in records).items())))
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(f'Built {len(ids)} entries: {len(originals)} original + {len(records)} Forever; {len(excluded)} excluded.')

if __name__ == '__main__':
    main()
