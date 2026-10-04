import json
import tempfile
import unittest
from pathlib import Path

from auth_utils import load_users, register_user, authenticate_user, save_users


class AuthUtilsTests(unittest.TestCase):
    def test_register_and_authenticate_user(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            users_file = Path(tmpdir) / "users.json"
            users = load_users(users_file)
            self.assertEqual(users, {})

            success, message = register_user("alice", "secret123", "Alice Smith", users_file)
            self.assertTrue(success)
            self.assertIn("registered successfully", message.lower())

            auth_user = authenticate_user("alice", "secret123", users_file)
            self.assertIsNotNone(auth_user)
            self.assertEqual(auth_user["username"], "alice")

            wrong_password = authenticate_user("alice", "wrong", users_file)
            self.assertIsNone(wrong_password)


if __name__ == "__main__":
    unittest.main()
