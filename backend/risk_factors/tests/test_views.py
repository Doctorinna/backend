import random

from .test_setup import TestSetUp
from risk_factors.models import Disease, Category, Range, Question, Option


class TestDiseaseView(TestSetUp):
    def test_get_diseases(self):
        response = self.client.get(self.diseases_url)
        self.assertEqual(response.status_code, 200)


class TestQuestionnaireView(TestSetUp):
    def test_get_categories(self):
        response = self.client.get(self.categories_url)
        self.assertEqual(response.status_code, 200)

    def test_get_questions(self):
        response = self.client.get(self.questions_url)
        self.assertEqual(response.status_code, 200)

    def test_get_questions_by_used_category(self):
        category = random.choice(self.categories_used)
        response = self.client.get(f'{self.questions_url}{category.title}/')
        self.assertEqual(response.status_code, 200)

    def test_get_questions_by_unused_category(self):
        categories_all = list(Category.objects.all())
        categories_titles = [c.title for c in categories_all]
        category_title = self.faker.word()
        while category_title in categories_titles:
            category_title = self.faker.word()
        response = self.client.get(f'{self.questions_url}{category_title}/')
        self.assertEqual(response.status_code, 404)
