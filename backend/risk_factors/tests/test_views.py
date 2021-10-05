from .test_setup import TestSetUp


class TestView(TestSetUp):
    def test_get_diseases(self):
        response = self.client.get(self.diseases)
        self.assertEqual(response.status_code, 200)
