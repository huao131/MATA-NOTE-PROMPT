from __future__ import annotations

import json
import tempfile
import unittest

from mata_studio.app import StudioApp
from mata_studio.context_package import build_context_package
from mata_studio.next_step import evaluate_next_step
from mata_studio.specifications import SpecificationResolver


class V11BridgeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.app = StudioApp(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_specification_resolver_reads_git_ref(self) -> None:
        resolver = SpecificationResolver(repo_root=self.temp.name, ref='HEAD')
        result = resolver.resolve(['README.md'])
        self.assertEqual(result['status'], 'SPECIFICATION_CONTEXT_UNAVAILABLE')

    def test_next_step_for_creative_input(self) -> None:
        state = evaluate_next_step(
            episode_id='EP003',
            brief={"episode_id": "EP003", "title": "測試"},
            production_state='AWAITING_CREATIVE_INPUT',
            gates={},
            artifacts=[],
            approvals={},
            locks={},
            rejected_assets=[],
            dependency_status={},
            drive_status={'status': 'NOT_CONNECTED'},
            specification_context={},
        )
        self.assertEqual(state['next_task_id'], 'AUDIENCE_INSIGHT_AND_CREATIVE_STRATEGY')

    def test_context_package_contains_required_fields(self) -> None:
        package = build_context_package(
            episode_id='EP003',
            brief={"episode_id": "EP003", "series_id": "SERIES", "title": "測試", "purpose": "測試", "target_audience": "測試", "duration_seconds": 30, "platform": "YouTube", "aspect_ratio": "9:16", "desired_action": "觀看", "existing_character_usage": "NONE", "special_requirements": []},
            production_state='AWAITING_CREATIVE_INPUT',
            gates={},
            artifacts=[],
            approvals={},
            locks={},
            rejected_assets=[],
            dependency_status={},
            drive_status={'status': 'NOT_CONNECTED'},
            specification_context={'source_ref': 'review/v2-system-specification-publication-v2', 'source_commit_sha': 'abc', 'sop_version': 'V2.0'},
            drive_mapping={'status': 'LOCAL_CONFIGURATION', 'episode_id': 'EP003', 'folders': {'01_專案控制': 'folder-1'}},
        )
        self.assertIn('SYSTEM_IDENTITY', package)
        self.assertIn('CURRENT_TASK', package)
        self.assertEqual(package['CURRENT_TASK']['task_id'], 'AUDIENCE_INSIGHT_AND_CREATIVE_STRATEGY')
        self.assertEqual(package['CURRENT_STATE']['drive_mapping']['episode_id'], 'EP003')
        self.assertEqual(package['CURRENT_STATE']['sync_status'], 'NOT_SYNCED')
        self.assertNotIn('approved_by', json.dumps(package))

    def test_next_step_blocks_when_specification_context_unavailable(self) -> None:
        state = evaluate_next_step(
            episode_id='EP003',
            brief={"episode_id": "EP003", "title": "測試"},
            production_state='AWAITING_CREATIVE_INPUT',
            gates={},
            artifacts=[],
            approvals={},
            locks={},
            rejected_assets=[],
            dependency_status={},
            drive_status={'status': 'NOT_CONNECTED'},
            specification_context={'status': 'SPECIFICATION_CONTEXT_UNAVAILABLE', 'reason': 'Git ref unavailable'},
        )
        self.assertEqual(state['status'], 'BLOCKED')
        self.assertIn('SPECIFICATION_CONTEXT_UNAVAILABLE', state['why_blocked'])

    def test_gate_pass_auto_advances_state(self) -> None:
        episode = self.app.create_episode({
            'episode_id': 'EP003',
            'series_id': 'SERIES',
            'series_name': '測試系列',
            'title': '測試',
            'purpose': '測試',
            'target_audience': '測試',
            'duration_seconds': 30,
            'platform': 'YouTube',
            'aspect_ratio': '9:16',
            'desired_action': '觀看',
            'existing_character_usage': 'NONE',
            'special_requirements': [],
        })
        self.app.submissions.submit(episode['episode_id'], {
            'episode_id': episode['episode_id'],
            'series_id': episode['series_id'],
            'artifact_type': 'CREATIVE_CANDIDATE',
            'version': 'V1.0',
            'lifecycle_status': 'DRAFT',
            'approval_status': 'PENDING_HUMAN_REVIEW',
            'lock_status': 'UNLOCKED',
            'production_state': 'CREATIVE_REVIEW',
            'source_asset_ids': [],
            'payload': {'content': 'ok'},
        })
        self.app.gates.submit(episode['episode_id'], 'creative_lock', 'V1.0')
        result = self.app.gates.decide(
            episode['episode_id'],
            'creative_lock',
            'PASS',
            {'approver': 'Mata老師', 'artifact_version': 'V1.0', 'evidence': '人工審閱', 'comment': '通過'},
        )
        self.assertEqual(result['gate_status'], 'PASS')
