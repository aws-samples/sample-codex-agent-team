#!/usr/bin/env python3
"""Regression tests for the fail-open subagent lifecycle hook."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("subagent_lifecycle.py")
MAX_LOG_BYTES = 1_048_576


class SubagentLifecycleTest(unittest.TestCase):
    def run_hook(
        self, raw_input: str
    ) -> tuple[subprocess.CompletedProcess[str], dict | None]:
        with tempfile.TemporaryDirectory() as home:
            env = os.environ.copy()
            env["HOME"] = home
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "start"],
                input=raw_input,
                text=True,
                capture_output=True,
                env=env,
                check=False,
            )
            log_path = Path(home) / ".codex/team-logs/subagent-events.jsonl"
            record = None
            if log_path.exists():
                record = json.loads(
                    log_path.read_text(encoding="utf-8").splitlines()[-1]
                )
            return result, record

    def test_non_object_json_is_treated_as_empty_payload(self) -> None:
        for raw_input in ("[]", "null", '"text"', "42"):
            with self.subTest(raw_input=raw_input):
                result, record = self.run_hook(raw_input)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIsNotNone(record)
                self.assertEqual(record["payload"], {})

    def test_malformed_json_is_treated_as_empty_payload(self) -> None:
        result, record = self.run_hook("{bad")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIsNotNone(record)
        self.assertEqual(record["payload"], {})

    def test_payload_keeps_only_allowed_keys(self) -> None:
        result, record = self.run_hook(
            '{"agent_id":"agent-1","model":"gpt-5.6-terra","secret":"drop"}'
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIsNotNone(record)
        self.assertEqual(
            record["payload"],
            {"agent_id": "agent-1", "model": "gpt-5.6-terra"},
        )

    def test_rotation_creates_a_persistent_sidecar_lock_file(self) -> None:
        with tempfile.TemporaryDirectory() as home:
            log_dir = Path(home) / ".codex/team-logs"
            log_dir.mkdir(parents=True)
            log_path = log_dir / "subagent-events.jsonl"
            log_path.write_text("x" * MAX_LOG_BYTES, encoding="utf-8")

            env = os.environ.copy()
            env["HOME"] = home
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "start"],
                input="{}",
                text=True,
                capture_output=True,
                env=env,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(
                log_path.with_name(f"{log_path.name}.lock").is_file(),
                "rotation must serialize through a persistent sidecar lock file",
            )

    def test_unavailable_log_path_is_fail_open(self) -> None:
        env = os.environ.copy()
        env["HOME"] = "/dev/null"

        result = subprocess.run(
            [sys.executable, str(SCRIPT), "start"],
            input="{}",
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
