import unittest
from cryptography.fernet import Fernet, InvalidToken

class FernetDemoTests(unittest.TestCase):
    def test_round_trip(self):
        key = Fernet.generate_key()
        cipher = Fernet(key)
        original = b"sample vault file"
        self.assertEqual(cipher.decrypt(cipher.encrypt(original)), original)

    def test_wrong_key_fails(self):
        cipher = Fernet(Fernet.generate_key())
        encrypted = cipher.encrypt(b"secret")
        other = Fernet(Fernet.generate_key())
        with self.assertRaises(InvalidToken):
            other.decrypt(encrypted)

if __name__ == "__main__":
    unittest.main()
