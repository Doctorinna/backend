from rest_framework.test import APITestCase
from django.urls import reverse
from risk_factors.models import Disease


class TestSetUp(APITestCase):
    def setUp(self):
        Disease.objects.create(illness='Sample disease',
                               description='Sample description')
        self.diseases = reverse('diseases')

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
