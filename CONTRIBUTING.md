# Contributing

Contributions are welcome when they improve the sample's clarity, safety, portability, or compatibility with current Codex behavior.

## Before Opening A Pull Request

1. Keep changes focused.
2. Do not commit local Codex runtime state, credentials, logs, caches, sessions, or SQLite files.
3. Update documentation when behavior changes.
4. Validate JSON, TOML, Python hooks, and plugin metadata.
5. Include the security impact of any new hook, MCP server, app integration, or executable script.

## Suggested Checks

```bash
python3 scripts/test_prompt_invariants.py -v
python3 .codex/hooks/test_subagent_lifecycle.py -v
python3 -m py_compile .codex/hooks/session_start.py .codex/hooks/subagent_lifecycle.py
python3 -m json.tool .codex/hooks.json
python3 -m json.tool .agents/plugins/marketplace.json
python3 -m json.tool plugins/codex-agent-team/.codex-plugin/plugin.json
python3 scripts/install_personal_plugin.py --dry-run
python3 -c "import pathlib, tomllib; files=[pathlib.Path('.codex/config.toml'), *pathlib.Path('.codex/agents').glob('*.toml')]; [tomllib.loads(p.read_text()) for p in files]"
ruby -e 'require "yaml"; ARGV.each { |f| YAML.load_file(f) }; puts "yaml ok"' plugins/codex-agent-team/skills/*/agents/openai.yaml
```

If available:

```bash
python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/codex-agent-team
```

## Pull Request Expectations

- Explain what changed and why.
- List validation commands and results.
- Call out any residual risk or intentionally unsupported case.
- Keep generated state out of the diff.
