#!/usr/bin/env python3
"""Regression tests for the public GPT-5.6 Codex agent-team guidance."""

from __future__ import annotations

import re
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / ".codex"
PLUGIN = ROOT / "plugins" / "codex-agent-team"

AGENTS = {
    "fullstack-agent": ("openai.gpt-5.6-sol", "xhigh", 1600),
    "review-agent": ("openai.gpt-5.6-sol", "max", 1000),
    "coding-agent": ("openai.gpt-5.6-terra", "xhigh", 700),
    "sa-agent": ("openai.gpt-5.6-terra", "max", 700),
    "devops-agent": ("openai.gpt-5.6-terra", "high", 1000),
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def missing_groups(path: Path, groups: tuple[tuple[str, ...], ...]) -> list[str]:
    text = read(path).lower()
    return [
        " | ".join(group)
        for group in groups
        if not any(term.lower() in text for term in group)
    ]


class PublicPromptInvariantTests(unittest.TestCase):
    maxDiff = None

    def assert_contract(
        self,
        path: Path,
        floor: int,
        groups: tuple[tuple[str, ...], ...],
    ) -> None:
        actual = words(read(path))
        self.assertGreaterEqual(
            actual,
            floor,
            f"{path} has {actual} words; regression floor is {floor}",
        )
        self.assertFalse(
            missing_groups(path, groups),
            f"{path} is missing required concepts: {missing_groups(path, groups)}",
        )

    def test_public_model_and_effort_matrix(self) -> None:
        self.assertFalse(
            (CODEX / "agents" / "test-suite-runner.toml").exists(),
            "The public repository intentionally excludes test-suite-runner",
        )
        for name, (model, effort, _) in AGENTS.items():
            with self.subTest(agent=name):
                data = tomllib.loads(read(CODEX / "agents" / f"{name}.toml"))
                self.assertEqual(data["name"], name)
                self.assertEqual(data["model"], model)
                self.assertEqual(data["model_reasoning_effort"], effort)

        config = tomllib.loads(read(CODEX / "config.toml"))
        self.assertEqual(config["model"], "openai.gpt-5.6-sol")
        self.assertEqual(config["model_reasoning_effort"], "xhigh")
        self.assertEqual(config["agents"]["max_threads"], 14)
        self.assertEqual(config["agents"]["max_depth"], 2)
        self.assertNotIn("model_provider", config)

    def test_global_guidance(self) -> None:
        self.assert_contract(
            ROOT / "AGENTS.md",
            650,
            (
                ("authorization",),
                ("non-interactive",),
                ("project-local", "dependency isolation"),
                ("durable artifacts",),
                ("file-disjoint",),
                ("positive evidence",),
                ("wait for all", "all requested agents"),
                ("close active agents", "close every"),
                ("active-worker check", "no required worker"),
                ("whole team run", "whole-run"),
                ("three review cycles", "three-cycle"),
                ("does not reset", "do not reset", "non-resetting"),
                ("verify the verifier",),
                ("live-validation gate", "live validation gate"),
                ("aws and production safety",),
            ),
        )

    def test_agent_contracts(self) -> None:
        requirements = {
            "fullstack-agent": (
                ("spawn plan",),
                ("implementation-phase entry gate", "build phase entry gate"),
                ("coding-agent", "coding-1"),
                ("up to 6", "cap: 6"),
                ("up to 2", "cap: 2"),
                ("up to 4", "cap: 4"),
                ("file-disjoint width",),
                ("wait for all requested agents", "wait for every requested agent"),
                ("positive evidence",),
                ("cycle 3 is terminal",),
                ("no required worker", "no agent remains active"),
                ("team-documentation",),
            ),
            "coding-agent": (
                ("team-spec-workflow",),
                ("exact file", "delegated file"),
                ("interface contract",),
                ("test-driven-development",),
                ("systematic-debugging",),
                ("concurrent-cached-fetch",),
                ("unit tests",),
                ("integration tests",),
                ("ci-blocking", "same checks ci"),
                ("mechanically",),
                ("aws-sdk-python-usage",),
                ("aws-sdk-js-v3-usage",),
                ("team-documentation",),
                ("residual risks",),
            ),
            "devops-agent": (
                ("explicit caller",),
                ("sourced defaults",),
                ("kube-context", "kubectl context"),
                ("authoritative backend", "real backend"),
                ("|| true",),
                ("independent residue", "independently query"),
                ("distinct destinations", "separate destination"),
                ("pipefail", "pipestatus"),
                ("todo placeholders",),
                ("kms",),
                ("egress",),
                ("classified storage", "data-classification"),
                ("eks access", "cluster-admin"),
                ("deploy/smoke/teardown", "deploy -> smoke -> teardown"),
                ("rollback",),
                ("runbook",),
            ),
            "review-agent": (
                ("synthesizer",),
                ("analyst",),
                ("spec alignment",),
                ("race",),
                ("cleanup",),
                ("empirically", "empirical"),
                ("before raising a critical", "before critical"),
                ("static-verifiable",),
                ("live-validation", "live validation"),
                ("verify the verifier",),
                ("cycle 1",),
                ("cycle 2",),
                ("cycle 3",),
                ("heartbeat", "still running"),
                ("pass or fail", "pass | fail"),
            ),
            "sa-agent": (
                ("engagement triggers",),
                ("state backend",),
                ("cloudwatch log",),
                ("classified storage", "data-classification"),
                ("egress",),
                ("eks access",),
                ("operational excellence",),
                ("performance efficiency",),
                ("cost optimization",),
                ("sustainability",),
                ("aws-mcp",),
                ("pricing",),
                ("regional availability",),
                ("owner",),
                ("rollout",),
                ("rollback",),
                ("residual risk",),
            ),
        }
        for name, groups in requirements.items():
            with self.subTest(agent=name):
                self.assert_contract(
                    CODEX / "agents" / f"{name}.toml",
                    AGENTS[name][2],
                    groups,
                )

    def test_skill_contracts(self) -> None:
        requirements = {
            "git-workflow": (
                400,
                (
                    ("non-interactive",),
                    ("conventional commits",),
                    ("merge conflict",),
                    ("worktree",),
                    ("pre-push",),
                    ("status --short",),
                    ("preserve user",),
                    ("reset --hard",),
                    ("force push",),
                    ("external writes",),
                ),
            ),
            "optimize-my-codex": (
                400,
                (
                    ("behavior-preserving",),
                    ("generated cache",),
                    ("exact model",),
                    ("line and word", "line/word"),
                    ("official codex",),
                    ("authoritative plugin source", "plugin source"),
                    ("skill metadata",),
                    ("success and failure", "both success and failure"),
                    ("byte", "deep comparison"),
                    ("representative",),
                    ("restart", "new-thread"),
                ),
            ),
            "team-brainstorm": (
                450,
                (
                    ("one focused question at a time",),
                    ("pain points",),
                    ("data volume",),
                    ("availability",),
                    ("latency",),
                    ("compliance",),
                    ("budget",),
                    ("timeline",),
                    ("deployment",),
                    ("failure scenarios",),
                    ("approval",),
                    ("interface",),
                    ("task wave",),
                    ("verification",),
                ),
            ),
            "team-spec-workflow": (
                450,
                (
                    ("requirements.md",),
                    ("spec.md",),
                    ("design.md",),
                    ("tasks.md",),
                    ("decisions.md",),
                    ("review.md",),
                    ("exact interfaces",),
                    ("file-disjoint",),
                    ("task status",),
                    ("live-validation", "live validation"),
                    ("fix wave",),
                    ("three-cycle", "three review cycles"),
                    ("close active agents", "no required worker remains active"),
                ),
            ),
            "team-coordination": (
                450,
                (
                    ("unique instance name",),
                    ("exact file scope",),
                    ("acceptance criteria",),
                    ("expected output",),
                    ("wait for all", "wait for every"),
                    ("positive evidence",),
                    ("quiet",),
                    ("stale",),
                    ("steer",),
                    ("close",),
                    ("active-worker", "no agent remains active"),
                    ("billable",),
                    ("degraded",),
                ),
            ),
            "team-review-cycle": (
                450,
                (
                    ("analyst",),
                    ("synthesizer",),
                    ("review.md",),
                    ("spec alignment",),
                    ("empirically", "empirical"),
                    ("verify the verifier",),
                    ("cycle 1",),
                    ("cycle 2",),
                    ("cycle 3",),
                    ("consumed when", "cycle is consumed"),
                    ("fix wave",),
                    ("terminal",),
                    ("close active agents", "close all"),
                ),
            ),
            "team-documentation": (
                450,
                (
                    ("readme",),
                    ("api",),
                    ("runbook",),
                    ("architecture decision", "adr"),
                    ("deployment",),
                    ("configuration",),
                    ("rollback",),
                    ("ownership",),
                    ("escalation",),
                    ("command examples",),
                    ("implementation names",),
                    ("staleness",),
                ),
            ),
        }
        for name, (floor, groups) in requirements.items():
            with self.subTest(skill=name):
                self.assert_contract(
                    PLUGIN / "skills" / name / "SKILL.md",
                    floor,
                    groups,
                )

    def test_command_boundaries(self) -> None:
        requirements = {
            "brainstorm.md": (("$arguments",), ("team-brainstorm",), ("requirements.md",), ("approval",)),
            "launch-codex-team.md": (
                ("$arguments",),
                ("team-coordination",),
                ("file-disjoint",),
                ("wait",),
                ("three-cycle",),
                ("close",),
            ),
            "optimize-my-codex.md": (
                ("$arguments",),
                ("optimize-my-codex",),
                ("approval",),
                ("behavior",),
                ("generated",),
            ),
        }
        for name, groups in requirements.items():
            with self.subTest(command=name):
                missing = missing_groups(PLUGIN / "commands" / name, groups)
                self.assertFalse(missing, f"{name} missing required concepts: {missing}")

    def test_skill_metadata(self) -> None:
        for directory in (
            "git-workflow",
            "optimize-my-codex",
            "team-brainstorm",
            "team-coordination",
            "team-documentation",
            "team-review-cycle",
            "team-spec-workflow",
        ):
            with self.subTest(skill=directory):
                text = read(PLUGIN / "skills" / directory / "agents" / "openai.yaml")
                self.assertIn("display_name:", text)
                self.assertIn("short_description:", text)
                self.assertIn("default_prompt:", text)

    def test_lifecycle_regression_is_published(self) -> None:
        self.assertTrue(
            (CODEX / "hooks" / "test_subagent_lifecycle.py").is_file(),
            "Publish the race/fail-open lifecycle regression with the hook",
        )

    def test_readme_contract(self) -> None:
        path = ROOT / "README.md"
        text = read(path).lower()
        for term in (
            "openai.gpt-5.6-sol",
            "openai.gpt-5.6-terra",
            "three-cycle",
            "scripts/test_prompt_invariants.py",
            "restart",
        ):
            self.assertIn(term, text)
        self.assertRegex(
            text,
            r"intentionally (excludes|does not include).*test-suite-runner",
        )
        self.assertNotIn("concise gpt-5.6-oriented developer instructions", text)

    def test_no_unqualified_claude_mechanism_claims(self) -> None:
        names = (
            "TaskCreate",
            "TaskUpdate",
            "TaskList",
            "TaskGet",
            "SendMessage",
            "verification sentinel",
            "persistent agent memory",
        )
        paths = [
            ROOT / "AGENTS.md",
            *(CODEX / "agents").glob("*.toml"),
            *(PLUGIN / "skills").glob("*/SKILL.md"),
            *(PLUGIN / "commands").glob("*.md"),
        ]
        allowed_markers = (
            "claude",
            "does not",
            "do not",
            "no shared",
            "not expose",
            "unavailable",
            "unsupported",
            "translate",
            "instead",
            "prohibit",
        )
        bad: list[str] = []
        for path in paths:
            for number, line in enumerate(read(path).splitlines(), 1):
                lower = line.lower()
                for name in names:
                    if name.lower() in lower and not any(
                        marker in lower for marker in allowed_markers
                    ):
                        bad.append(f"{path}:{number}: {line.strip()}")
        self.assertFalse(
            bad,
            "Claude-only mechanisms are claimed without an explicit "
            f"translation/prohibition:\n{chr(10).join(bad)}",
        )


if __name__ == "__main__":
    unittest.main()
