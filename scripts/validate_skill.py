"""Validate the published skill package without invoking an agent."""

from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'repo-testing-ci'
text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
frontmatter = re.match(r'\A---\n(.*?)\n---\n', text, re.DOTALL)
if frontmatter is None:
    raise SystemExit('Skill frontmatter is missing or malformed')
metadata = yaml.safe_load(frontmatter.group(1))
if not isinstance(metadata, dict) or metadata.get('name') != SKILL.name:
    raise SystemExit('Skill identity is invalid')
description = metadata.get('description')
if not isinstance(description, str) or not description.strip() or len(description) > 1024:
    raise SystemExit('Skill description is missing or invalid')
if not text[frontmatter.end():].strip():
    raise SystemExit('Skill instructions are empty')

agent = yaml.safe_load((SKILL / 'agents' / 'openai.yaml').read_text(encoding='utf-8'))
if not isinstance(agent, dict) or not isinstance(agent.get('interface'), dict):
    raise SystemExit('Agent interface is missing')
interface = agent['interface']
for field in ('display_name', 'short_description', 'default_prompt'):
    if not isinstance(interface.get(field), str) or not interface[field].strip():
        raise SystemExit('Agent interface field is missing: ' + field)
if not 25 <= len(interface['short_description']) <= 64:
    raise SystemExit('Agent short description has an invalid length')
if '$repo-testing-ci' not in interface['default_prompt']:
    raise SystemExit('Agent default prompt does not invoke the skill')

for document in (ROOT / 'README.md', SKILL / 'SKILL.md'):
    for target in re.findall(r'\]\(([^)]+)\)', document.read_text(encoding='utf-8')):
        parsed = urlsplit(target.strip('<>'))
        if parsed.scheme or not parsed.path:
            continue
        destination = (document.parent / unquote(parsed.path)).resolve()
        if not destination.is_relative_to(ROOT) or not destination.exists():
            raise SystemExit('Broken or nonportable link: ' + target)

print('Skill identity, instructions, agent metadata, and local links pass.')
