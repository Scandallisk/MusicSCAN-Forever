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
from catalog_identity import normalized_identity

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
    original_records = []
    for line in originals:
        original_records.append({key: json.loads(value) for key, value in re.findall(
            r'(\w+)=("(?:[^"\\]|\\.)*"|false|true|\d+)', line)})
    originals_by_id = {r['fileDataID']: r for r in original_records}
    identity_index = {}
    for record in original_records:
        for identity in {normalized_identity(record['sourceFilename']), normalized_identity(record['title'])}:
            identity_index.setdefault(identity, {})[record['fileDataID']] = record
    overrides = json.loads((ROOT / 'tools/catalog-duplicate-overrides.json').read_text(encoding='utf-8'))
    duplicates, kept = [], []
    applied_overrides = set()
    for record in records:
        matches = {}
        for identity in {normalized_identity(record['sourceFilename']), normalized_identity(record['title'])}:
            matches.update(identity_index.get(identity, {}))
        override = overrides.get(str(record['fileDataID']))
        if override:
            canonical = originals_by_id[override['canonicalID']]
            if matches and set(matches) != {canonical['fileDataID']}:
                raise SystemExit('Duplicate override conflicts with normalized identity.')
            reason = override['reason']
            applied_overrides.add(str(record['fileDataID']))
        elif len(matches) == 1:
            canonical = next(iter(matches.values()))
            reason = 'exact-normalized-filename-or-title'
        elif matches:
            raise SystemExit(f'Ambiguous duplicate identity: {record["sourceFilename"]}')
        else:
            kept.append(record)
            continue
        duplicates.append(dict(aliasID=record['fileDataID'], canonicalID=canonical['fileDataID'],
                               aliasKey=record['key'], canonicalKey=canonical['key'],
                               aliasTitle=record['title'], canonicalTitle=canonical['title'],
                               aliasPath=record['sourceFilename'], canonicalPath=canonical['sourceFilename'],
                               reason=reason))
    if applied_overrides != set(overrides):
        raise SystemExit('A reviewed duplicate override no longer matches the source; review it.')
    original_count, source_forever_count = len(original_records), len(records)
    for record in original_records:
        record['expansion'] = 'World of Warcraft: Forever'
    records = original_records + kept
    ids = [r['fileDataID'] for r in records]
    keys = [r['key'] for r in records]
    assert len(ids) == len(set(ids)) and len(keys) == len(set(keys))
    # Variations remain distinct: compare full normalized titles, including numbers/day/night.
    display_identities = [(normalized_identity(r['zone']), normalized_identity(r['title'])) for r in records]
    assert len(display_identities) == len(set(display_identities)), 'Repeated named catalog entry'
    records.sort(key=lambda r: (r['zone'].lower(), r['title'].lower(), r['fileDataID']))
    text = ('-- MusicSCAN Forever alpha: metadata only; no bundled audio.\n'
            '-- Filename-derived labels are provisional; see SOURCES.md.\nlocal _, ns = ...\n\n'
            'ns.ExpansionOrder = { ["World of Warcraft: Forever"] = 1 }\n\nns.Catalog = {\n')
    for record in records:
        fields = []
        for key, value in record.items():
            encoded = 'false' if value is False else str(value) if isinstance(value, int) else lua_string(value)
            fields.append(f'{key}={encoded}')
        text += '    {' + ', '.join(fields) + '},\n'
    text += '}\n\nns.DEFAULT_TRACK_KEY = ' + lua_string(original_keys[0]) + '\n'
    text += '\n-- Metadata-equivalent legacy/Forever files share one browser row; old saved IDs still resolve.\n'
    text += 'ns.FileIDAliases = {\n'
    for pair in sorted(duplicates, key=lambda r: r['aliasID']):
        text += f'    [{pair["aliasID"]}] = {pair["canonicalID"]},\n'
    text += '}\nns.TrackKeyAliases = {\n'
    for pair in sorted(duplicates, key=lambda r: r['aliasKey']):
        text += f'    [{lua_string(pair["aliasKey"])}] = {lua_string(pair["canonicalKey"])},\n'
    text += '}\n'
    (ADDON / 'Database.lua').write_text(text, encoding='utf-8')
    with (ROOT / 'catalog/FOREVER-CATALOG.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    manifest_path = ROOT / 'catalog/CATALOG-SOURCE.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    version = re.search(r'^## Version: (.+)$', (ADDON / 'MusicSCAN.toc').read_text(), re.M)[1].strip()
    manifest.update(version=version, originalCount=original_count, foreverCount=len(kept), total=len(ids),
                    sourceForeverCount=source_forever_count, duplicateCount=len(duplicates),
                    categoryCount=1, identityBasis='normalized-metadata-and-reviewed-filename-aliases',
                    audioContentCompared=False,
                    excludedCount=len(excluded), excluded=excluded,
                    zoneCounts=dict(sorted(Counter(r['zone'] for r in records).items())))
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    with (ROOT / 'catalog/DUPLICATE-AUDIT.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=['aliasID','canonicalID','aliasKey','canonicalKey',
                                                   'aliasTitle','canonicalTitle','aliasPath','canonicalPath','reason'])
        writer.writeheader()
        writer.writerows(sorted(duplicates, key=lambda r: r['canonicalID']))
    print(f'Built {len(ids)} entries in one Forever category: {original_count} original + {len(kept)} additional; '
          f'{len(duplicates)} metadata duplicates consolidated; {len(excluded)} cues excluded.')

if __name__ == '__main__':
    main()
