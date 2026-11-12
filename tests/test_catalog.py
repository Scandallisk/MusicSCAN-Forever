"""Protect source identities, distinct variations and the reviewed duplicate audit."""
import csv
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from catalog_identity import normalized_identity


def parse_records(text):
    return [{key: json.loads(value) for key, value in re.findall(
        r'(\w+)=("(?:[^"\\]|\\.)*"|false|true|\d+)', line)}
        for line in text.splitlines() if line.lstrip().startswith('{key=')]


class CatalogAuditTests(unittest.TestCase):
    def test_all_original_identities_survive_category_move(self):
        originals = parse_records((ROOT / 'catalog/original-wow-records.txt').read_text(encoding='utf-8'))
        current = parse_records((ROOT / 'MusicSCAN/Database.lua').read_text(encoding='utf-8'))
        by_key = {track['key']: track for track in current}
        self.assertEqual(len(originals), 200)
        self.assertEqual(len(current), 415)
        for record in originals:
            expected = dict(record, expansion='World of Warcraft: Forever')
            self.assertEqual(by_key[record['key']], expected)

    def test_no_repeated_ids_source_names_or_named_rows(self):
        current = parse_records((ROOT / 'MusicSCAN/Database.lua').read_text(encoding='utf-8'))
        for values in ([r['key'] for r in current], [r['fileDataID'] for r in current],
                       [normalized_identity(r['sourceFilename']) for r in current],
                       [(normalized_identity(r['zone']), normalized_identity(r['title'])) for r in current]):
            self.assertEqual(len(values), len(set(values)))
        self.assertEqual({r['expansion'] for r in current}, {'World of Warcraft: Forever'})

    def test_duplicate_audit_keeps_only_canonical_records(self):
        current = parse_records((ROOT / 'MusicSCAN/Database.lua').read_text(encoding='utf-8'))
        by_id = {r['fileDataID']: r for r in current}
        with (ROOT / 'catalog/DUPLICATE-AUDIT.csv').open(encoding='utf-8', newline='') as handle:
            audit = list(csv.DictReader(handle))
        self.assertEqual(len(audit), 155)
        self.assertEqual(len({r['aliasID'] for r in audit}), 155)
        self.assertEqual(sum("AhnQiraj" in r['aliasPath'] for r in audit), 17)
        for pair in audit:
            self.assertNotIn(int(pair['aliasID']), by_id)
            self.assertEqual(by_id[int(pair['canonicalID'])]['key'], pair['canonicalKey'])

    def test_variations_remain_distinct(self):
        self.assertEqual(normalized_identity('Ahn Qiraj Exterior Walking 1'),
                         normalized_identity("Ahn'Qiraj Exterior Walking 1"))
        for first, second in [('Hyjal General A', 'Hyjal General B'),
                              ('Forest Day 1', 'Forest Night 1'),
                              ('Interior 1', 'Interior 2'),
                              ('Stormwind 1 Moment', 'Stormwind 1 Zone'),
                              ('Tavern 1A', 'Tavern 1B')]:
            self.assertNotEqual(normalized_identity(first), normalized_identity(second))


if __name__ == '__main__':
    unittest.main()
