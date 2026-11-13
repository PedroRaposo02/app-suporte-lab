import unittest

from app import is_healthy


class HealthTests(unittest.TestCase):
    def test_estado_saudavel(self):
        self.assertTrue(is_healthy("status=HEALTHY"))

    def test_estado_invalido(self):
        self.assertFalse(is_healthy("status=WARNING"))


if __name__ == "__main__":
    unittest.main()
