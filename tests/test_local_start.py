import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]

class FakeFlask:
    def __init__(self, *args, **kwargs):
        self.settings = None
    def route(self, *args, **kwargs):
        return lambda function: function
    def run(self, **kwargs):
        self.settings = kwargs

class LocalStartTests(unittest.TestCase):
    def test_server_uses_isolated_data_and_local_defaults(self):
        with tempfile.TemporaryDirectory() as directory:
            data = str(Path(directory) / 'data with spaces')
            fake = SimpleNamespace(Flask=FakeFlask, render_template=None, request=None, jsonify=None)
            env = {k: v for k, v in os.environ.items() if not k.startswith('AI_PAPER_')}
            env['AI_PAPER_DATA_DIR'] = data
            with patch.dict(os.environ, env, clear=True), patch.dict(sys.modules, flask=fake):
                module = runpy.run_path(str(ROOT / 'flask_server.py'), run_name='__main__')
            self.assertEqual(module['app'].settings, dict(host='127.0.0.1', port=8082, debug=False))
            target = Path(module['LIKED_PAPERS_FILE'])
            self.assertEqual(target.parent, Path(data))
            module['write_json'](target, {'synthetic': 1})
            self.assertEqual(module['read_json'](target), {'synthetic': 1})

    def test_launcher_from_other_cwd_with_spaces_and_exit_status(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'viewer with spaces'
            root.mkdir()
            shutil.copy(ROOT / 'serve.sh', root / 'serve.sh')
            (root / 'flask_server.py').write_text('# synthetic')
            fake = root / 'fake python'
            fake.write_text('#!/bin/sh\nprintf "%s" "$1" > "$ARG_LOG"\nexit 7\n')
            fake.chmod(0o700)
            log = root / 'argument'
            result = subprocess.run(['bash', str(root / 'serve.sh')], cwd='/',
                env=dict(os.environ, AI_PAPER_PYTHON=str(fake), ARG_LOG=str(log)), timeout=5)
            self.assertEqual(result.returncode, 7)
            self.assertEqual(log.read_text(), str(root / 'flask_server.py'))

if __name__ == '__main__':
    unittest.main()
