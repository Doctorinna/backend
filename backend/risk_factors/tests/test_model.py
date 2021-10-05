from .test_setup import TestSetUp
from risk_factors.models import Disease


class TestModel(TestSetUp):
    def test_disease_to_string(self):
        disease = Disease.objects.get(illness='Sample disease')
        self.assertEqual(str(disease), 'Sample disease')
