# AgentSupply

An MIT-licensed marketplace for skills you can install in Codex and Claude Code.

[`repo-testing-ci`](skills/repo-testing-ci/SKILL.md) is the first skill. It discovers the repository's stack and conventions, keeps implementation and tests together, diagnoses CI failures, and gives pull requests a clear validation summary.

## Install

### Codex

Add the marketplace and install AgentSupply:

```sh
codex plugin marketplace add cybrking/agent-supply
codex plugin add agent-supply@agent-supply
```

To install only `repo-testing-ci`, ask Codex:

```text
$skill-installer Install https://github.com/cybrking/agent-supply/tree/main/skills/repo-testing-ci
```

The installer preserves an existing installation. The skill is available on the next turn after installation.

### Claude Code

```sh
claude plugin marketplace add cybrking/agent-supply
claude plugin install agent-supply@agent-supply
```

### Manual installation

Clone this repository and copy the [skill directory](skills/repo-testing-ci) into your agent's skills directory. For Codex's default installation location:

```sh
git clone https://github.com/cybrking/agent-supply.git
mkdir -p ~/.codex/skills
test ! -e ~/.codex/skills/repo-testing-ci && \
  cp -R agent-supply/skills/repo-testing-ci ~/.codex/skills/
```

For Claude Code, use `~/.claude/skills/` as the destination. If the destination already exists, compare and update it deliberately; the command above leaves it untouched.

## Use

From the repository you want to work on:

```text
$repo-testing-ci
Review this repository's testing and CI. Report gaps without changing files.
```

Or authorize implementation and publication explicitly:

```text
$repo-testing-ci
Implement the missing regression coverage, run the relevant checks,
and open a pull request with the code, tests, fixtures, and CI changes together.
```

For the marketplace install, invoke `$agent-supply:repo-testing-ci` in Codex or `/agent-supply:repo-testing-ci` in Claude Code. For a manual install in Claude Code, invoke `/repo-testing-ci`.

The skill uses existing project tools. Recommended ECC and shipping skills are optional; it specifies an equivalent workflow when those skills are unavailable. It does not grant permission to publish, merge, deploy, or change production systems merely by being invoked.

## PR descriptions

The default format is:

- **Summary:** the problem and resulting behavior.
- **Changes:** a short list of concrete changes.
- **Validation:** a Check / Result / Evidence table with actual results and CI links.
- **Risks / remaining work:** material limitations and unverified behavior.

Detailed commands and revision evidence belong in linked verification notes. Required repository templates and explicit user instructions take precedence. See the [complete skill](skills/repo-testing-ci/SKILL.md#pr-description-format).

## Validate this package

Maintainer checks require Python 3.10 or later and PyYAML:

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_skill.py
python3 -B -m unittest discover -s tests -v
```

GitHub Actions runs the same checks on Python 3.10 and 3.14. They validate skill and agent metadata, local Markdown links, portable package paths, and rejection of executable YAML. They do not run a model or prove agent behavior in every host.

## License

[MIT](LICENSE).
