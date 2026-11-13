import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import urlopen

from app import Handler, is_healthy


class HealthTests(unittest.TestCase):
    def test_estado_saudavel(self):
        self.assertTrue(is_healthy("status=HEALTHY"))

    def test_estado_invalido(self):
        self.assertFalse(is_healthy("status=WARNING"))


class HealthEndpointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.base_url = f"http://127.0.0.1:{cls.server.server_address[1]}"
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_rota_health_responde_200(self):
        with urlopen(f"{self.base_url}/health", timeout=2) as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(response.read().decode("utf-8"), "status=HEALTHY\n")

    def test_rota_inexistente_responde_404(self):
        with self.assertRaises(HTTPError) as ctx:
            urlopen(f"{self.base_url}/inexistente", timeout=2)
        self.assertEqual(ctx.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
