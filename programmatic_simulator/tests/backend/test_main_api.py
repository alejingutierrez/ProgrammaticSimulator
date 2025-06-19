import unittest
from programmatic_simulator.backend.main import app

class TestMainAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_market_data(self):
        resp = self.client.get('/api/market-data')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn('marcas', data)
        self.assertIn('audiencias', data)
        self.assertIn('campaign_goals', data)

    def test_interests_data(self):
        resp = self.client.get('/api/interests-data')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

if __name__ == '__main__':
    unittest.main()
