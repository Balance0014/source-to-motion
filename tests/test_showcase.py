"""Cross-category behavior check: the visual center changes, not just the HUD."""
import importlib.util
import json
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ('uv', 'ollama', 'trivy', 'duckdb', 'tailscale', 'excalidraw')


class ShowcaseBehavior(unittest.TestCase):
    def test_each_public_source_has_two_visible_hero_changes(self):
        for name in PROJECTS:
            with self.subTest(project=name):
                directory = ROOT / 'examples' / name
                facts = {f['id']: f for f in json.loads((directory/'facts.json').read_text())['facts']}
                source = json.loads((directory/'source.json').read_text())
                self.assertIn('raw.githubusercontent.com', source['locator'])
                self.assertTrue(all(f['evidence'] in source['text'] for f in facts.values()))
                self.assertTrue(all(f'detail_{i}' in facts for i in range(1, 7)),
                                f'{name}: product-specific perimeter content missing')
                self.assertEqual(facts['stars']['display'].replace(',', ''),
                                 str(source['github_snapshot']['stars']))
                self.assertEqual(facts['forks']['display'].replace(',', ''),
                                 str(source['github_snapshot']['forks']))
                self.assertIn(source['github_snapshot']['captured_at_utc'][:10],
                              facts['snapshot_date']['display'])
                spec = importlib.util.spec_from_file_location('showcase_'+name, directory/'scene.py')
                scene = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(scene)
                self.assertEqual(scene.SIZE, (1080, 1350))
                samples = [np.asarray(scene.render(t, facts).crop((40,215,730,990)).resize((90,100)),
                                      dtype=np.int16) for t in (1.2, 5.8, 10.2)]
                early = float(np.abs(samples[1]-samples[0]).mean())
                late = float(np.abs(samples[2]-samples[1]).mean())
                self.assertGreater(early, 10, f'{name}: center stays still in early beat')
                self.assertGreater(late, 10, f'{name}: center stays still in final beat')


if __name__ == '__main__':
    unittest.main()
