
import unittest
from mata_studio.chatgpt_import import ChatGPTImportParser
from mata_studio.errors import StudioError

class TestChatGPTImportParser(unittest.TestCase):
    def setUp(self):
        self.parser = ChatGPTImportParser(store=None)

    def test_pure_json_success(self):
        raw = '{"episode_id": "EP001", "artifact_type": "CREATIVE_CANDIDATE", "version": "V1.0"}'
        payload = self.parser.import_payload("EP001", raw)
        self.assertEqual(payload['artifact_type'], 'CREATIVE_CANDIDATE')

    def test_markdown_block_success(self):
        raw = '說明文字\n```json\n{"episode_id": "EP001", "artifact_type": "CREATIVE_CANDIDATE", "version": "V1.0"}\n```'
        payload = self.parser.import_payload("EP001", raw)
        self.assertEqual(payload['artifact_type'], 'CREATIVE_CANDIDATE')

    def test_multiple_different_json_conflict(self):
        raw = '{"episode_id": "EP001", "artifact_type": "CREATIVE_CANDIDATE", "version": "V1.0"} {"episode_id": "EP001", "artifact_type": "STORY_TREATMENT", "version": "V1.0"}'
        with self.assertRaises(StudioError) as cm:
            self.parser.import_payload("EP001", raw)
        self.assertEqual(cm.exception.code, "MULTIPLE_JSON_OBJECTS_CONFLICT")

    def test_duplicate_json_success(self):
        raw = '{"episode_id": "EP001", "artifact_type": "CREATIVE_CANDIDATE", "version": "V1.0"} {"episode_id": "EP001", "artifact_type": "CREATIVE_CANDIDATE", "version": "V1.0"}'
        payload = self.parser.import_payload("EP001", raw)
        self.assertEqual(payload['artifact_type'], 'CREATIVE_CANDIDATE')

    def test_text_with_braces_not_confused(self):
        raw = '說明文字包含 {大括號} 但 JSON 是 {"episode_id": "EP001", "artifact_type": "CREATIVE_CANDIDATE", "version": "V1.0"}'
        payload = self.parser.import_payload("EP001", raw)
        self.assertEqual(payload['artifact_type'], 'CREATIVE_CANDIDATE')

    def test_array_rejected(self):
        raw = '[{"episode_id": "EP001", "artifact_type": "CREATIVE_CANDIDATE", "version": "V1.0"}]'
        with self.assertRaises(StudioError) as cm:
            self.parser.import_payload("EP001", raw)
        self.assertEqual(cm.exception.code, "NO_JSON_FOUND")

    def test_no_json_found(self):
        raw = '純文字說明'
        with self.assertRaises(StudioError) as cm:
            self.parser.import_payload("EP001", raw)
        self.assertEqual(cm.exception.code, "NO_JSON_FOUND")
