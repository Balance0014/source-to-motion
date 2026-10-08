"""Meaningful contract checks; no external network calls."""

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import wave
from pathlib import Path

from PIL import ImageChops

ROOT = Path(__file__).resolve().parents[1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


ingest = module("stm_ingest", "ingest.py")
verify = module("stm_verify", "verify.py")


class PipelineContracts(unittest.TestCase):
    def test_gapmine_snapshot_accepts_grouping_but_rejects_changed_count(self):
        facts_path = ROOT / "examples/gapmine/facts.json"
        source_path = ROOT / "examples/gapmine/source.json"
        self.assertEqual(verify.verify_facts(facts_path, source_path), 22)
        altered = json.loads(facts_path.read_text())
        next(f for f in altered["facts"] if f["id"] == "cards")["display"] = "1,141"
        with tempfile.TemporaryDirectory() as folder:
            bad = Path(folder) / "facts.json"
            bad.write_text(json.dumps(altered))
            with self.assertRaisesRegex(ValueError, "numbers absent"):
                verify.verify_facts(bad, source_path)

    def test_chinese_video_evidence_and_distinct_beats(self):
        facts_path = ROOT / "examples/pulse-atlas-zh/facts.json"
        source_path = ROOT / "examples/pulse-atlas/source.json"
        self.assertEqual(verify.verify_facts(facts_path, source_path), 12)
        facts = {f["id"]: f for f in json.loads(facts_path.read_text())["facts"]}
        spec = importlib.util.spec_from_file_location("stm_scene_zh", ROOT/"examples/pulse-atlas-zh/scene.py")
        zh_scene = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(zh_scene)
        intro = zh_scene.render(1.2, facts)
        board = zh_scene.render(9.0, facts)
        self.assertEqual(intro.size, (960, 540))
        self.assertIsNotNone(ImageChops.difference(intro, board).getbbox())

    @unittest.skipUnless(shutil.which("ffmpeg"), "FFmpeg is required")
    def test_render_and_verify_with_short_audio(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            scene = root / "scene.py"
            scene.write_text(
                "from PIL import Image, ImageDraw\n"
                "SIZE=(640,360)\nFPS=12\nDURATION=1.0\n"
                "def render(t,facts):\n"
                " im=Image.new('RGB',SIZE,'#101c2c')\n"
                " d=ImageDraw.Draw(im)\n"
                " d.ellipse((int(100+t*180),100,int(180+t*180),180),fill='#4ce3d1')\n"
                " d.text((30,30),facts['count']['display'],fill='white')\n"
                " return im\n"
            )
            facts = root / "facts.json"
            source = root / "source.json"
            facts.write_text(json.dumps({"facts":[{"id":"count","display":"12","evidence":"12 incidents","locator":"fixture"}]}))
            source.write_text(json.dumps({"text":"12 incidents processed."}))
            audio = root / "audio.wav"
            with wave.open(str(audio), "wb") as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(48000)
                wav.writeframes(b"\x00\x00" * 9600)  # 0.2 s for a 1.0 s video
            video = root / "video.mp4"
            subprocess.run([sys.executable, str(ROOT/"scripts/render.py"), "--scene", str(scene),
                            "--facts", str(facts), "--audio", str(audio), "--out", str(video)],
                           check=True, timeout=30, capture_output=True)
            details = verify.video_details(video)
            self.assertAlmostEqual(details["duration"], 1.0, places=1)
            self.assertTrue(details["audio"])
            self.assertEqual(verify.verify_facts(facts, source), 1)
            sheet = root / "contact.jpg"
            verify.contact_sheet(video, sheet, details["duration"])
            self.assertTrue(sheet.is_file())

    def test_docx_extracts_exact_metrics(self):
        source = ingest.extract(str(ROOT / "examples/pulse-atlas/brief.docx"))
        self.assertEqual(source["kind"], "docx")
        for marker in ("2,480", "97.4%", "12 minutes"):
            self.assertIn(marker, source["text"])

    def test_pdf_extracts_exact_metrics(self):
        source = ingest.extract(str(ROOT / "examples/pulse-atlas/brief.pdf"))
        self.assertEqual(source["kind"], "pdf")
        for marker in ("2,480", "97.4%", "12 minutes"):
            self.assertIn(marker, source["text"])

    def test_manifest_passes_and_tampered_number_fails(self):
        facts_path = ROOT / "examples/pulse-atlas/facts.json"
        source_path = ROOT / "examples/pulse-atlas/source.json"
        self.assertEqual(verify.verify_facts(facts_path, source_path), 10)
        bad = json.loads(facts_path.read_text())
        next(f for f in bad["facts"] if f["id"] == "tagging")["display"] = "99.9%"
        with tempfile.TemporaryDirectory() as folder:
            altered = Path(folder) / "facts.json"
            altered.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError, "numbers absent"):
                verify.verify_facts(altered, source_path)

    def test_unquoted_evidence_fails(self):
        facts_path = ROOT / "examples/uv/facts.json"
        source_path = ROOT / "examples/uv/source.json"
        facts = json.loads(facts_path.read_text())
        facts["facts"][0]["evidence"] = "a billion times faster"
        with tempfile.TemporaryDirectory() as folder:
            altered = Path(folder) / "facts.json"
            altered.write_text(json.dumps(facts))
            with self.assertRaisesRegex(ValueError, "not found"):
                verify.verify_facts(altered, source_path)


if __name__ == "__main__":
    unittest.main()
