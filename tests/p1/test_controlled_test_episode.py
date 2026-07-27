from __future__ import annotations

import json
import unittest
from collections.abc import Mapping
from pathlib import Path

from ._support import SRC  # noqa: F401
from mata_p0.asset_index import (
    assert_asset_usage,
    assert_exact_asset_operation,
    validate_asset_index,
)
from mata_p0.dependency_recheck import (
    assert_gate_allowed,
    validate_recheck_record,
)
from mata_p0.errors import ContractViolation, StopAndReport
from mata_p0.folder_registry import validate_folder_registry
from mata_p0.repository_governance import assert_p0_write_path
from mata_p0.schema_validation import (
    require_enum,
    require_fields,
    require_list,
    require_mapping,
)
from mata_p0.version_lock import (
    assert_file_operation_allowed,
    assert_unique_versions,
    validate_supersession,
)
from mata_p1.episode_initialization import validate_episode_initialization_plan
from mata_p1.gate_register import validate_gate_register
from mata_p1.handoff_manifest import validate_handoff_manifest
from mata_p1.production_state import validate_state_proposal
from mata_p1.prompt_metadata import validate_prompt_metadata
from mata_p1.status_handling import validate_status


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests" / "p1" / "fixtures" / "CONTROLLED_TEST_EPISODE"


SCHEMA_LOCATIONS = {
    "episode_initialization.schema.json": ROOT / "schemas" / "p1",
    "production_state.schema.json": ROOT / "schemas" / "p1",
    "gate_register.schema.json": ROOT / "schemas" / "p1",
    "segment_asset_status.schema.json": ROOT / "schemas" / "p1",
    "prompt_library_metadata.schema.json": ROOT / "schemas" / "p1",
    "storyboard_flow_handoff.schema.json": ROOT / "schemas" / "p1",
    "folder_registry.schema.json": ROOT / "schemas" / "p0",
    "asset_index.schema.json": ROOT / "schemas" / "p0",
    "dependency_recheck.schema.json": ROOT / "schemas" / "p0",
}

ENVELOPE_FIELDS = (
    "test_only",
    "test_namespace",
    "episode_id",
    "plan_id",
    "operation",
    "schema_name",
    "contract_type",
    "permitted_scope_values",
    "selected_scope_value",
)


def fixture(name: str):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def stop(code: str, path: str, message: str):
    raise StopAndReport(ContractViolation(code, path, message))


def validate_schema_node(value, definition, path="$"):
    if "enum" in definition:
        require_enum(value, definition["enum"], path)
    if "const" in definition and value != definition["const"]:
        stop("CONST_MISMATCH", path, "value violates Schema const")

    expected = definition.get("type")
    if isinstance(expected, list):
        if value is None and "null" in expected:
            return value
        expected = next((item for item in expected if item != "null"), None)

    if expected == "object":
        record = require_mapping(value, path)
        require_fields(record, definition.get("required", ()), path)
        properties = definition.get("properties", {})
        if definition.get("additionalProperties") is False:
            extras = sorted(set(record) - set(properties))
            if extras:
                stop(
                    "ADDITIONAL_PROPERTY_FORBIDDEN",
                    path,
                    f"unexpected formal Payload fields: {extras}",
                )
        for field, child in properties.items():
            if field in record:
                validate_schema_node(record[field], child, f"{path}.{field}")
    elif expected == "array":
        records = require_list(value, path)
        minimum = definition.get("minItems", 0)
        maximum = definition.get("maxItems")
        if len(records) < minimum or (
            maximum is not None and len(records) > maximum
        ):
            stop("ARRAY_LENGTH_INVALID", path, "array length violates Schema")
        item_schema = definition.get("items")
        if item_schema:
            for index, item in enumerate(records):
                validate_schema_node(item, item_schema, f"{path}[{index}]")
    elif expected == "string":
        if not isinstance(value, str):
            stop("SCHEMA_TYPE_ERROR", path, "expected string")
        if len(value) < definition.get("minLength", 0):
            stop("SCHEMA_STRING_LENGTH", path, "string is too short")
    elif expected == "integer":
        if isinstance(value, bool) or not isinstance(value, int):
            stop("SCHEMA_TYPE_ERROR", path, "expected integer")
        if value < definition.get("minimum", value):
            stop("SCHEMA_MINIMUM", path, "integer is below minimum")
    elif expected == "boolean" and not isinstance(value, bool):
        stop("SCHEMA_TYPE_ERROR", path, "expected boolean")
    return value


def validate_formal_shape(value, schema_name: str):
    schema_dir = SCHEMA_LOCATIONS.get(schema_name)
    if schema_dir is None:
        stop("UNKNOWN_SCHEMA", "$.schema_name", "scope contract cannot be guessed")
    schema = json.loads((schema_dir / schema_name).read_text(encoding="utf-8"))
    return validate_schema_node(value, schema, "$.payload")


def validate_envelope(value):
    envelope = require_mapping(value, "$")
    require_fields(envelope, ENVELOPE_FIELDS)
    if envelope["test_only"] is not True:
        stop("TEST_ONLY_REQUIRED", "$.test_only", "test wrapper must be isolated")
    if envelope["test_namespace"] != "TEST_CONTROLLED_EPISODE_001":
        stop("TEST_NAMESPACE_INVALID", "$.test_namespace", "unexpected namespace")
    if envelope["episode_id"] != "TEST_EP_P0P1_001":
        stop("TEST_EPISODE_ID_INVALID", "$.episode_id", "unexpected TEST Episode")
    if envelope["plan_id"] != "TEST_PLAN_P0P1_001":
        stop("TEST_PLAN_ID_INVALID", "$.plan_id", "unexpected TEST Plan")
    if envelope["operation"] != "VALIDATE_PLAN":
        stop("TEST_OPERATION_INVALID", "$.operation", "execution is not authorized")

    schema_name = envelope["schema_name"]
    if schema_name not in SCHEMA_LOCATIONS:
        stop("UNKNOWN_SCHEMA", "$.schema_name", "scope contract cannot be guessed")

    payload_values = (
        list(envelope["payloads"].values())
        if "payloads" in envelope
        else [envelope.get("payload")]
    )
    for payload_value in payload_values:
        if isinstance(payload_value, Mapping) and {
            "test_only",
            "test_namespace",
            "approval_type",
        }.intersection(payload_value):
            stop(
                "TEST_METADATA_PAYLOAD_LEAK",
                "$.payload",
                "test control Metadata cannot enter formal Payload",
            )
        validate_formal_shape(payload_value, schema_name)

    schema_dir = SCHEMA_LOCATIONS[schema_name]
    schema = json.loads((schema_dir / schema_name).read_text(encoding="utf-8"))
    formal_scope = schema.get("properties", {}).get("scope_type", {}).get("enum")
    if formal_scope is not None:
        permitted = envelope["permitted_scope_values"]
        if list(permitted) != list(formal_scope):
            stop(
                "SCOPE_CONTRACT_CONFLICT",
                "$.permitted_scope_values",
                "wrapper scope values must exactly follow its formal Schema",
            )
    return envelope


def validate_layer_scope(payload, expected_scope: str):
    validate_formal_shape(payload, "production_state.schema.json")
    if payload["scope_type"] != expected_scope:
        stop(
            "SCOPE_LAYER_MISMATCH",
            "$.payload.scope_type",
            f"{expected_scope} data must use {expected_scope}",
        )
    return payload


class ControlledTestEpisode(unittest.TestCase):
    maxDiff = None

    def assert_structured_stop(self, callable_, *args, **kwargs):
        with self.assertRaises(StopAndReport) as context:
            callable_(*args, **kwargs)
        self.assertTrue(context.exception.violations)
        for violation in context.exception.violations:
            self.assertTrue(violation.code)
            self.assertIsInstance(violation.path, str)
            self.assertTrue(violation.message)

    def gate_records(self):
        return fixture("TEST_GATE_REGISTER.json")["payload"]

    def state_record(self, layer="episode"):
        return fixture("TEST_PRODUCTION_STATE_CANDIDATE.json")["payloads"][layer]

    def status_record(self):
        return fixture("TEST_SEGMENT_ASSET_STATUS.json")["payload"]

    def prompt_record(self):
        return fixture("TEST_PROMPT_LIBRARY_METADATA.json")["payload"]

    def handoff_record(self):
        return fixture("TEST_STORYBOARD_FLOW_HANDOFF.json")["payload"]

    # Positive cases and P0/P1 integration chain.
    def test_positive_01_episode_initialization(self):
        envelope = validate_envelope(fixture("TEST_EPISODE_INITIALIZATION.json"))
        record = envelope["payload"]
        self.assertEqual(record["episode_id"], "TEST_EP_P0P1_001")
        self.assertEqual(validate_episode_initialization_plan(record), record)

    def test_positive_02_verified_dependency_pass_state_candidate(self):
        validate_envelope(fixture("TEST_PRODUCTION_STATE_CANDIDATE.json"))
        record = self.state_record()
        self.assertTrue(validate_state_proposal(record)["canonical_candidate"])

    def test_positive_02b_segment_state_candidate(self):
        record = validate_layer_scope(self.state_record("segment"), "SEGMENT")
        self.assertFalse(validate_state_proposal(record)["canonical_candidate"])

    def test_positive_02c_asset_state_candidate(self):
        record = validate_layer_scope(self.state_record("asset"), "ASSET")
        self.assertFalse(validate_state_proposal(record)["canonical_candidate"])

    def test_positive_03_six_gates_in_fixed_order(self):
        envelope = validate_envelope(fixture("TEST_GATE_REGISTER.json"))
        records = self.gate_records()
        self.assertEqual(len(validate_gate_register(records)), 6)
        self.assertEqual(
            [record["gate_id"] for record in records],
            [
                "creative_lock",
                "story_lock",
                "story_visual_lock",
                "keyframe_lock",
                "production_lock",
                "final_approved",
            ],
        )
        self.assertTrue(
            all(
                record["approved_by"] == "HUMAN_TEST_APPROVER"
                and record["basis_documents"] == ["TEST_ONLY_SIMULATED_APPROVAL"]
                for record in records
            )
        )
        self.assertEqual(
            envelope["simulated_approval"]["approval_type"],
            "TEST_ONLY_SIMULATED_APPROVAL",
        )

    def test_positive_04_lifecycle_and_qc_are_separate(self):
        record = validate_status(self.status_record())
        self.assertEqual(record["lifecycle_status"], "REVIEW")
        self.assertEqual(record["qc_status"], "PASS")

    def test_positive_05_reference_asset_allowed(self):
        record = self.status_record()
        assert_asset_usage(record, "REFERENCE")

    def test_positive_06_exact_asset_original_file_preserved(self):
        asset = fixture("TEST_ASSET_INDEX.json")["payload"]["assets"][1]
        assert_exact_asset_operation(
            asset,
            proposed_drive_file_id=asset["approved_original_drive_file_id"],
            generated_or_redrawn=False,
        )

    def test_positive_07_prompt_metadata_complete(self):
        self.assertEqual(
            validate_prompt_metadata(self.prompt_record())["scope"],
            "TEST_CONTROLLED_EPISODE_001",
        )

    def test_positive_08_handoff_manifest_complete(self):
        envelope = validate_envelope(
            fixture("TEST_STORYBOARD_FLOW_HANDOFF.json")
        )
        record = validate_handoff_manifest(self.handoff_record())
        self.assertEqual(
            envelope["simulated_approval"]["approval_type"],
            "TEST_ONLY_SIMULATED_APPROVAL",
        )

    def test_positive_09_upstream_change_creates_recheck(self):
        record = fixture("TEST_DEPENDENCY_RECHECK.json")["payload"]
        validate_recheck_record(record)
        self.assertEqual(record["recheck_result"], "DEPENDENCY_RECHECK_REQUIRED")

    def test_positive_10_recheck_pass_restores_gate_eligibility(self):
        record = fixture("TEST_DEPENDENCY_RECHECK.json")["payload"]
        record["recheck_result"] = "PASS"
        assert_gate_allowed("PASS", record)

    def test_positive_11_folder_registry_and_asset_index_contracts(self):
        folders = fixture("TEST_FOLDER_REGISTRY.json")["payload"]["folders"]
        registry = validate_folder_registry(
            folders,
            enforce_current_effective=False,
        )
        assets = fixture("TEST_ASSET_INDEX.json")["payload"]["assets"]
        index = validate_asset_index(assets, registry)
        self.assertEqual(
            set(index),
            {"TEST_AST_REFERENCE_001", "TEST_AST_EXACT_001"},
        )
        self.assertTrue(all("filename" not in record for record in assets))

    def test_positive_12_version_and_supersession_contracts(self):
        old = {
            "scope_id": "TEST_CONTROLLED_EPISODE_001",
            "artifact_id": "TEST_AST_REFERENCE_001",
            "version": "TEST_VERSION_V1.0",
        }
        new = dict(old, version="TEST_VERSION_V2.0")
        assert_unique_versions([old, new])
        validate_supersession(old, new)

    def test_positive_13_schema_documents_are_valid_json(self):
        schema_paths = tuple((ROOT / "schemas" / "p0").glob("*.json")) + tuple(
            (ROOT / "schemas" / "p1").glob("*.json")
        )
        self.assertTrue(schema_paths)
        for path in schema_paths:
            with self.subTest(path=path):
                self.assertIsInstance(
                    json.loads(path.read_text(encoding="utf-8")),
                    dict,
                )

    def test_positive_14_protected_and_repository_guards_allow_safe_probe(self):
        assert_file_operation_allowed("WRITE", "src/mata_p0/example.py")
        self.assertEqual(
            assert_p0_write_path("tests/p0/fixtures/TEST_SAFE.json"),
            "tests/p0/fixtures/TEST_SAFE.json",
        )

    def test_positive_15_all_fixtures_map_to_explicit_contracts(self):
        for path in sorted(FIXTURES.glob("*.json")):
            with self.subTest(path=path.name):
                envelope = validate_envelope(
                    json.loads(path.read_text(encoding="utf-8"))
                )
                self.assertIn(envelope["schema_name"], SCHEMA_LOCATIONS)

    # Required negative cases. Every failure must use structured STOP_AND_REPORT.
    def test_negative_01_formal_episode_id(self):
        record = fixture("TEST_EPISODE_INITIALIZATION.json")["payload"]
        record["episode_id"] = "EP99"
        self.assert_structured_stop(validate_episode_initialization_plan, record)

    def test_negative_02_test_scope_without_test_prefix(self):
        record = fixture("TEST_EPISODE_INITIALIZATION.json")["payload"]
        record["scope_id"] = "CONTROLLED_EPISODE_001"
        self.assert_structured_stop(validate_episode_initialization_plan, record)

    def test_negative_02a_initialization_rejects_episode_scope(self):
        record = fixture("TEST_EPISODE_INITIALIZATION.json")["payload"]
        record["scope_type"] = "EPISODE"
        self.assert_structured_stop(validate_episode_initialization_plan, record)

    def test_negative_02b_initialization_rejects_segment_scope(self):
        record = fixture("TEST_EPISODE_INITIALIZATION.json")["payload"]
        record["scope_type"] = "SEGMENT"
        self.assert_structured_stop(validate_episode_initialization_plan, record)

    def test_negative_02c_initialization_rejects_asset_scope(self):
        record = fixture("TEST_EPISODE_INITIALIZATION.json")["payload"]
        record["scope_type"] = "ASSET"
        self.assert_structured_stop(validate_episode_initialization_plan, record)

    def test_negative_02d_initialization_rejects_unknown_scope(self):
        record = fixture("TEST_EPISODE_INITIALIZATION.json")["payload"]
        record["scope_type"] = "TEST_UNKNOWN_SCOPE"
        self.assert_structured_stop(validate_episode_initialization_plan, record)

    def test_negative_02e_initialization_missing_required_field(self):
        record = fixture("TEST_EPISODE_INITIALIZATION.json")["payload"]
        del record["owner"]
        self.assert_structured_stop(validate_episode_initialization_plan, record)

    def test_negative_02f_initialization_formal_write_operation(self):
        record = fixture("TEST_EPISODE_INITIALIZATION.json")["payload"]
        record["operation"] = "WRITE_FORMAL_EPISODE"
        self.assert_structured_stop(validate_episode_initialization_plan, record)

    def test_negative_02g_production_state_rejects_test_scope(self):
        record = self.state_record()
        record["scope_type"] = "TEST"
        self.assert_structured_stop(
            validate_formal_shape,
            record,
            "production_state.schema.json",
        )

    def test_negative_02h_production_state_rejects_plan_candidate_scope(self):
        record = self.state_record()
        record["scope_type"] = "PLAN_CANDIDATE"
        self.assert_structured_stop(
            validate_formal_shape,
            record,
            "production_state.schema.json",
        )

    def test_negative_02i_episode_layer_rejects_segment_scope(self):
        record = self.state_record()
        record["scope_type"] = "SEGMENT"
        self.assert_structured_stop(validate_layer_scope, record, "EPISODE")

    def test_negative_02j_segment_layer_rejects_asset_scope(self):
        record = self.state_record("segment")
        record["scope_type"] = "ASSET"
        self.assert_structured_stop(validate_layer_scope, record, "SEGMENT")

    def test_negative_02k_asset_layer_rejects_episode_scope(self):
        record = self.state_record("asset")
        record["scope_type"] = "EPISODE"
        self.assert_structured_stop(validate_layer_scope, record, "ASSET")

    def test_negative_02l_test_metadata_cannot_leak_into_formal_payload(self):
        envelope = fixture("TEST_EPISODE_INITIALIZATION.json")
        envelope["payload"]["test_only"] = True
        self.assert_structured_stop(validate_envelope, envelope)

    def test_negative_02m_unknown_schema_stops_without_guessing_scope(self):
        envelope = fixture("TEST_EPISODE_INITIALIZATION.json")
        envelope["schema_name"] = "TEST_UNKNOWN_SCHEMA.json"
        self.assert_structured_stop(validate_envelope, envelope)

    def test_negative_02n_schema_scope_conflict_has_no_inferred_priority(self):
        envelope = fixture("TEST_EPISODE_INITIALIZATION.json")
        envelope["permitted_scope_values"] = ["EPISODE", "SEGMENT", "ASSET"]
        self.assert_structured_stop(validate_envelope, envelope)

    def test_negative_03_inferred_canonical_candidate(self):
        record = self.state_record()
        record["evidence_status"] = "INFERRED"
        self.assert_structured_stop(validate_state_proposal, record)

    def test_negative_04_unverified_gate_pass(self):
        records = self.gate_records()
        records[0]["evidence_status"] = "UNVERIFIED"
        self.assert_structured_stop(validate_gate_register, records)

    def test_negative_05_conflicted_evidence_cannot_continue(self):
        record = self.state_record()
        record["evidence_status"] = "CONFLICTED"
        self.assert_structured_stop(validate_state_proposal, record)

    def test_negative_06_dependency_not_pass_gate(self):
        records = self.gate_records()
        records[0]["dependency_recheck_result"] = "PENDING"
        self.assert_structured_stop(validate_gate_register, records)

    def test_negative_07_predecessor_not_pass(self):
        records = self.gate_records()
        records[0]["gate_status"] = "PENDING"
        self.assert_structured_stop(validate_gate_register, records)

    def test_negative_08_codex_approver(self):
        records = self.gate_records()
        records[0]["approved_by"] = "CODEX"
        self.assert_structured_stop(validate_gate_register, records)

    def test_negative_09_gate_item_not_mapping(self):
        records = self.gate_records()
        records[2] = "TEST_NOT_A_MAPPING"
        self.assert_structured_stop(validate_gate_register, records)

    def test_negative_10_missing_approved_version(self):
        records = self.gate_records()
        del records[0]["approved_version"]
        self.assert_structured_stop(validate_gate_register, records)

    def test_negative_11_missing_approved_by(self):
        records = self.gate_records()
        del records[0]["approved_by"]
        self.assert_structured_stop(validate_gate_register, records)

    def test_negative_12_missing_approved_at(self):
        records = self.gate_records()
        del records[0]["approved_at"]
        self.assert_structured_stop(validate_gate_register, records)

    def test_negative_13_missing_basis_documents(self):
        records = self.gate_records()
        del records[0]["basis_documents"]
        self.assert_structured_stop(validate_gate_register, records)

    def test_negative_14_segment_ready_cannot_promote_episode(self):
        record = self.state_record()
        record.update(
            {
                "segment_status": "READY",
                "current_episode_status": "IN_PROGRESS",
                "episode_status": "READY",
                "episode_ready_basis": "SEGMENT_READY",
            }
        )
        self.assert_structured_stop(validate_state_proposal, record)

    def test_negative_15_lifecycle_and_qc_mixed(self):
        record = self.status_record()
        record["qc_status"] = "REVIEW"
        self.assert_structured_stop(validate_status, record)

    def test_negative_16_rejected_reference(self):
        record = self.status_record()
        record["lifecycle_status"] = "REJECTED"
        self.assert_structured_stop(validate_status, record)

    def test_negative_17_rejected_dependency(self):
        record = self.status_record()
        record["lifecycle_status"] = "REJECTED"
        record["usage_roles"] = ["DEPENDENCY"]
        self.assert_structured_stop(validate_status, record)

    def test_negative_18_exact_asset_file_replaced(self):
        record = self.status_record()
        record.update(
            {
                "asset_id": "TEST_AST_EXACT_001",
                "exact_asset": True,
                "approved_original_drive_file_id": "TEST_DRIVE_FILE_EXACT_001",
                "proposed_drive_file_id": "TEST_DRIVE_FILE_REPLACEMENT_001",
            }
        )
        self.assert_structured_stop(validate_status, record)

    def test_negative_19_exact_asset_generated_or_redrawn(self):
        record = self.status_record()
        record.update(
            {
                "asset_id": "TEST_AST_EXACT_001",
                "exact_asset": True,
                "approved_original_drive_file_id": "TEST_DRIVE_FILE_EXACT_001",
                "proposed_drive_file_id": "TEST_DRIVE_FILE_EXACT_001",
                "generated_or_redrawn": True,
            }
        )
        self.assert_structured_stop(validate_status, record)

    def test_negative_20_prompt_content_forbidden(self):
        record = self.prompt_record()
        record["prompt_content"] = "TEST_FORBIDDEN_PROMPT_BODY"
        self.assert_structured_stop(validate_prompt_metadata, record)

    def test_negative_21_prompt_flow_command_forbidden(self):
        record = self.prompt_record()
        record["flow_command"] = "TEST_FORBIDDEN_FLOW_COMMAND"
        self.assert_structured_stop(validate_prompt_metadata, record)

    def test_negative_22_prompt_execute_flow_forbidden(self):
        record = self.prompt_record()
        record["execute_flow"] = True
        self.assert_structured_stop(validate_prompt_metadata, record)

    def test_negative_23_handoff_flow_execution_forbidden(self):
        record = self.handoff_record()
        record["execute_flow"] = True
        self.assert_structured_stop(validate_handoff_manifest, record)

    def test_negative_24_handoff_capcut_operation_forbidden(self):
        record = self.handoff_record()
        record["capcut_operation"] = "TEST_FORBIDDEN_OPERATION"
        self.assert_structured_stop(validate_handoff_manifest, record)

    def test_negative_25_handoff_media_generation_forbidden(self):
        record = self.handoff_record()
        record["generate_media"] = True
        self.assert_structured_stop(validate_handoff_manifest, record)

    def test_negative_26_repository_path_traversal(self):
        self.assert_structured_stop(
            assert_p0_write_path,
            "tests/p0/../../episodes/EP99/TEST.json",
        )

    def test_negative_27_episodes_write_forbidden(self):
        self.assert_structured_stop(
            assert_p0_write_path,
            "episodes/TEST_EP_P0P1_001/TEST.json",
        )

    def test_negative_28_system_write_forbidden(self):
        self.assert_structured_stop(
            assert_p0_write_path,
            "system/TEST_CONTROLLED_EPISODE_001.json",
        )

    def test_negative_29_templates_write_forbidden(self):
        self.assert_structured_stop(
            assert_p0_write_path,
            "templates/TEST_CONTROLLED_EPISODE_001.json",
        )

    def test_negative_30_formal_canonical_state_attempt(self):
        record = self.state_record()
        record["scope_id"] = "EP99"
        record["evidence_status"] = "INFERRED"
        self.assert_structured_stop(validate_state_proposal, record)

    def test_schema_specific_scope_resolution_is_consistent(self):
        initialization = validate_envelope(
            fixture("TEST_EPISODE_INITIALIZATION.json")
        )
        production = validate_envelope(
            fixture("TEST_PRODUCTION_STATE_CANDIDATE.json")
        )
        self.assertEqual(
            initialization["permitted_scope_values"],
            ["TEST", "PLAN_CANDIDATE"],
        )
        self.assertEqual(
            production["permitted_scope_values"],
            ["EPISODE", "SEGMENT", "ASSET"],
        )


if __name__ == "__main__":
    unittest.main()
