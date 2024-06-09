import hashlib
import shutil
import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from tinydb import TinyDB, Query
import crud
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestApp(unittest.TestCase):
    """
    Test suite for the Artefact Management System.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up test class by creating test directories and files.
        """
        cls.test_data_path = 'test_data/'
        if not os.path.exists(cls.test_data_path):
            os.makedirs(cls.test_data_path)
        cls.lyrics_db = TinyDB(os.path.join(cls.test_data_path, 'lyrics.json'))
        # Create a valid test image
        os.makedirs('images', exist_ok=True)
        with open('images/example.png', 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\xdac\xf8\x0f\x04\x00\x05\xfe\x02\xfe\xe2\x00\x00\x00\x00IEND\xaeB`\x82')

    @classmethod
    def tearDownClass(cls):
        """
        Tear down test class by removing test directories and files.
        """
        if os.path.exists('images'):
            shutil.rmtree('images')
        if os.path.exists(cls.test_data_path):
            shutil.rmtree(cls.test_data_path)

    def setUp(self):
        """
        Set up test case by truncating the test database.
        """
        self.lyrics_db.truncate()

    def test_create_artefact(self):
        """
        Test the creation of an artefact.
        """
        artefact = {
            'title': 'Test Song',
            'content': 'La la la'
        }
        user = 'user1'
        role = 'user'
        artefact_id = crud.create_artefact(self.lyrics_db, artefact, user, role)
        self.assertEqual(artefact_id, 1)
        artefacts = crud.read_artefacts(self.lyrics_db, user, role)
        self.assertEqual(len(artefacts), 1)
        self.assertEqual(artefacts[0]['title'], 'Test Song')

    def test_read_artefacts(self):
        """
        Test reading artefacts.
        """
        artefact = {
            'title': 'Test Song',
            'content': 'La la la'
        }
        user = 'user1'
        role = 'user'
        crud.create_artefact(self.lyrics_db, artefact, user, role)
        artefacts = crud.read_artefacts(self.lyrics_db, user, role)
        self.assertEqual(len(artefacts), 1)
        self.assertEqual(artefacts[0]['title'], 'Test Song')

    def test_update_artefact(self):
        """
        Test updating an artefact.
        """
        artefact = {
            'title': 'Test Song',
            'content': 'La la la'
        }
        user = 'user1'
        role = 'user'
        artefact_id = crud.create_artefact(self.lyrics_db, artefact, user, role)
        updated_artefact = {
            'title': 'Updated Song',
            'content': 'Do re mi'
        }
        crud.update_artefact(self.lyrics_db, artefact_id, updated_artefact, user, role)
        artefacts = crud.read_artefacts(self.lyrics_db, user, role)
        self.assertEqual(artefacts[0]['title'], 'Updated Song')

    def test_delete_artefact(self):
        """
        Test deleting an artefact.
        """
        artefact = {
            'title': 'Test Song',
            'content': 'La la la'
        }
        user = 'user1'
        role = 'user'
        artefact_id = crud.create_artefact(self.lyrics_db, artefact, user, role)
        crud.delete_artefact(self.lyrics_db, artefact_id, user, role)
        artefacts = crud.read_artefacts(self.lyrics_db, user, role)
        self.assertEqual(len(artefacts), 0)

    def test_create_artefact_with_thumbnail(self):
        """
        Test creating an artefact with a thumbnail.
        """
        artefact = {
            'title': 'Test Song',
            'content': 'La la la'
        }
        image_path = 'images/example.png'
        category = 'lyrics'
        user = 'user1'
        role = 'user'
        artefact_id = crud.create_artefact_with_thumbnail(self.lyrics_db, artefact, image_path, category, user, role)
        self.assertEqual(artefact_id, 1)
        thumbnail_path = os.path.join('data/thumbnails/lyrics', f'{artefact_id}.png')
        self.assertTrue(os.path.exists(thumbnail_path))

    def test_update_artefact_permission(self):
        """
        Test updating an artefact with insufficient permissions.
        """
        artefact = {
            'title': 'Test Song',
            'content': 'La la la'
        }
        user1 = 'user1'
        user2 = 'user2'
        role1 = 'user'
        role2 = 'user'
        artefact_id = crud.create_artefact(self.lyrics_db, artefact, user1, role1)
        updated_artefact = {
            'title': 'Updated Song',
            'content': 'Do re mi'
        }
        with self.assertRaises(PermissionError):
            crud.update_artefact(self.lyrics_db, artefact_id, updated_artefact, user2, role2)

    def test_delete_artefact_permission(self):
        """
        Test deleting an artefact with insufficient permissions.
        """
        artefact = {
            'title': 'Test Song',
            'content': 'La la la'
        }
        user1 = 'user1'
        user2 = 'user2'
        role1 = 'user'
        role2 = 'user'
        artefact_id = crud.create_artefact(self.lyrics_db, artefact, user1, role1)
        with self.assertRaises(PermissionError):
            crud.delete_artefact(self.lyrics_db, artefact_id, user2, role2)

    def test_admin_delete_artefact(self):
        """
        Test deleting an artefact with admin permissions.
        """
        artefact = {
            'title': 'Test Song',
            'content': 'La la la'
        }
        user = 'user1'
        admin = 'admin'
        role_user = 'user'
        role_admin = 'admin'
        artefact_id = crud.create_artefact(self.lyrics_db, artefact, user, role_user)
        crud.delete_artefact(self.lyrics_db, artefact_id, admin, role_admin)
        artefacts = crud.read_artefacts(self.lyrics_db, admin, role_admin)
        self.assertEqual(len(artefacts), 0)

    def test_invalid_role(self):
        """
        Test creating an artefact with an invalid role.
        """
        artefact = {
            'title': 'Test Song',
            'content': 'La la la'
        }
        user = 'user1'
        invalid_role = 'invalid_role'
        with self.assertRaises(ValueError):
            crud.create_artefact(self.lyrics_db, artefact, user, invalid_role)

    def test_checksum_calculation(self):
        """
        Test checksum calculation.
        """
        content = 'Content to hash'
        checksum = crud.calculate_checksum(content)
        expected_checksum = hashlib.sha256(content.encode('utf-8')).hexdigest()
        self.assertEqual(checksum, expected_checksum)

    def test_verify_checksum_success(self):
        """
        Test successful checksum verification.
        """
        content = 'Content to hash'
        checksum = crud.calculate_checksum(content)
        self.assertTrue(crud.verify_checksum(content, checksum))

    def test_verify_checksum_failure(self):
        """
        Test failed checksum verification.
        """
        content = 'Content to hash'
        wrong_checksum = 'incorrectchecksum'
        self.assertFalse(crud.verify_checksum(content, wrong_checksum))

if __name__ == '__main__':
    unittest.main()
