"""Exercise Flask routing and persistence using only temporary synthetic data."""
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SERVER = Path(__file__).resolve().parents[1] / 'flask_server.py'

def load_server(data):
    with patch.dict(os.environ, AI_PAPER_DATA_DIR=data):
        spec = importlib.util.spec_from_file_location('viewer_test', SERVER)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

class HTTPTests(unittest.TestCase):
    def test_routes_and_restart_persistence(self):
        with tempfile.TemporaryDirectory() as directory:
            module = load_server(directory)
            client = module.app.test_client()
            self.assertEqual(client.get('/').status_code, 200)
            self.assertEqual(client.get('/get_data').json['liked_papers'], {})
            self.assertEqual(client.post('/like', json={}).status_code, 400)
            self.assertEqual(client.post('/like', json={'paper_id': 'synthetic'}).json['likes'], 1)
            self.assertEqual(client.post('/mark_read', json={'paper_id': 'synthetic'}).status_code, 200)
            self.assertEqual(client.post('/add_to_list', json={'paper_id': 'synthetic', 'list_name': 'test'}).status_code, 200)
            restarted = load_server(directory).app.test_client()
            data = restarted.get('/get_data').json
            self.assertEqual(data['liked_papers'], {'synthetic': 1})
            self.assertEqual(data['paper_lists']['readed'], ['synthetic'])
            self.assertEqual(data['paper_lists']['test'], ['synthetic'])
            self.assertEqual(restarted.post('/unread', json={'paper_id': 'synthetic'}).status_code, 200)
            self.assertEqual(restarted.get('/get_data').json['paper_lists']['readed'], [])

if __name__ == '__main__':
    unittest.main()
