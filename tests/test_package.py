from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='skill package ')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for name in ('README.md', 'scripts/validate_skill.py',
                     'skills/repo-testing-ci/SKILL.md',
                     'skills/repo-testing-ci/agents/openai.yaml'):
            destination = self.root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, destination)

    def validate(self):
        return subprocess.run([sys.executable, '-B', str(self.root / 'scripts/validate_skill.py')],
                              cwd=self.root, capture_output=True, text=True, timeout=10)

    def test_portable_package_from_unrelated_directory(self):
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_agent_metadata_and_broken_links_fail(self):
        agent = self.root / 'skills/repo-testing-ci/agents/openai.yaml'
        original = agent.read_bytes()
        agent.write_text('interface: {}\n')
        self.assertNotEqual(self.validate().returncode, 0)
        agent.write_bytes(original)
        (self.root / 'README.md').write_text('[Missing instructions](missing.md)\n')
        self.assertNotEqual(self.validate().returncode, 0)

    def test_yaml_cannot_execute_a_constructor(self):
        sentinel = self.root / 'EXECUTED'
        agent = self.root / 'skills/repo-testing-ci/agents/openai.yaml'
        agent.write_text('!!python/object/apply:builtins.exec\n- "open(\'EXECUTED\', \'w\').close()"\n')
        self.assertNotEqual(self.validate().returncode, 0)
        self.assertFalse(sentinel.exists())


if __name__ == '__main__':
    unittest.main()
