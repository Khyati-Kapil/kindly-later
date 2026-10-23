import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import kindly_later as app


class KindlyLaterTests(unittest.TestCase):
    def setUp(self):
        self.message = app.Message("x.eml", "A <a@example.test>", "Question", "", "Can you send the notes?")

    def test_exact_evidence_required(self):
        with self.assertRaises(ValueError):
            app.validate_suggestion({"decision": "reply", "reason": "Asked", "evidence": "Send me the notes", "draft": "Sure"}, self.message)

    def test_reply_requires_draft(self):
        with self.assertRaises(ValueError):
            app.validate_suggestion({"decision": "reply", "reason": "Asked", "evidence": "Can you send the notes?", "draft": ""}, self.message)

    def test_question_cannot_be_ignored(self):
        with self.assertRaisesRegex(ValueError, "question"):
            app.validate_suggestion({"decision": "ignore", "reason": "No action", "evidence": "Can you send the notes?", "draft": ""}, self.message)

    def test_render_escapes_untrusted_email_and_model_text(self):
        message = app.Message("x.eml", "<script>alert(1)</script>", "<img src=x onerror=alert(1)>", "", "Can you send the notes?")
        html = app.render_report([(message, {"decision": "reply", "reason": "<script>bad()</script>", "evidence": "Can you send the notes?", "draft": "<b>Thanks</b>"})], "gemma3:4b")
        self.assertNotIn("<script>bad()</script>", html)
        self.assertNotIn("<b>Thanks</b>", html)
        self.assertIn("&lt;b&gt;Thanks&lt;/b&gt;", html)

    def test_reads_plain_text_sample(self):
        sample = Path(__file__).resolve().parents[1] / "examples/mail/01-coffee.eml"
        message = app.read_message(sample)
        self.assertIn("Are you free for coffee", message.body)

    def test_integration_with_fake_model_and_review_fallback(self):
        sample = Path(__file__).resolve().parents[1] / "examples/mail/01-coffee.eml"
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp) / "mail"
            folder.mkdir()
            (folder / "sample.eml").write_bytes(sample.read_bytes())
            report = Path(temp) / "report.html"
            with patch.object(app, "ask_model", return_value={"decision": "reply", "reason": "Question", "evidence": "Are you free for coffee", "draft": "Friday might work; what time?"}):
                self.assertEqual(app.run(folder, report, "fake"), 0)
            self.assertIn("Friday might work", report.read_text())
            with patch.object(app, "ask_model", return_value={"decision": "reply", "reason": "Question", "evidence": "fabricated", "draft": "Yes"}):
                app.run(folder, report, "fake")
            self.assertIn("Review manually", report.read_text())


if __name__ == "__main__":
    unittest.main()
