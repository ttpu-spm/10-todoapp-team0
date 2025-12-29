import unittest
import json
import os
import sys

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from app import app, DATA_FILE

class TodoAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Use a temporary file for tests
        self.test_db = 'test_todos.json'
        app.config['DATA_FILE'] = self.test_db
        # Monkey patch the DATA_FILE in app module (since it's a global variable there)
        import app as app_module
        app_module.DATA_FILE = self.test_db
        
        # Ensure clean state
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
            
        # Reset in-memory list if needed (though app reloads from file)
        app_module.todos = []

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Todo App', response.data)

    def test_add_todo(self):
        response = self.app.post('/add', data=dict(content='Test Todo'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Todo', response.data)
        
        # Verify persistence
        with open(self.test_db, 'r') as f:
            data = json.load(f)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]['content'], 'Test Todo')

    def test_delete_todo(self):
        # Add a todo first
        self.app.post('/add', data=dict(content='Delete Me'), follow_redirects=True)
        
        # Get the ID (it should be 1)
        response = self.app.get('/delete/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Delete Me', response.data)

    def test_toggle_todo(self):
        self.app.post('/add', data=dict(content='Toggle Me'), follow_redirects=True)
        
        response = self.app.get('/toggle/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Check if it's marked as completed (class "completed")
        # Note: This checks HTML output, might be fragile if class name changes
        # Better to check the file
        with open(self.test_db, 'r') as f:
            data = json.load(f)
            self.assertTrue(data[0]['completed'])

if __name__ == '__main__':
    unittest.main()
