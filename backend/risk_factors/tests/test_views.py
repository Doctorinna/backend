import random
import json

from .test_setup import TestSetUp
from risk_factors.models import Category, Question, Result


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
        response = self.client.get(f'{self.questions_url}{category.title}')
        self.assertEqual(response.status_code, 200)

    def test_get_questions_by_unused_category(self):
        categories_all = list(Category.objects.all())
        categories_titles = [c.title for c in categories_all]
        category_title = self.faker.word()
        while category_title in categories_titles:
            category_title = self.faker.word()
        response = self.client.get(f'{self.questions_url}{category_title}')
        self.assertEqual(response.status_code, 404)

    def test_post_response_survey(self):
        questions = list(Question.objects.all())
        survey_response_obj = []
        for question in questions:
            response_obj = {
                'question': question.id,
                'answer': self.faker.word()
            }
            survey_response_obj.append(response_obj)

        response = self.client.post(self.response_url,
                                    json.dumps(survey_response_obj),
                                    content_type='application/json')
        self.client.session.save()
        self.assertEqual(response.status_code, 201)

        results = list(Result.objects.all())
        result = random.choice(results)
        session = result.session
        true_output = f"{session}: {result.disease} - {result.risk_factor}"
        self.assertEqual(str(result), true_output)

        response = self.client.get(self.response_url)
        self.assertEqual(response.status_code, 200)

        random_question = random.choice(questions)
        response_changed = {
            'question': random_question.id,
            'answer': self.faker.word()
        }
        response = self.client.put(f'{self.response_url}{random_question.id}',
                                   json.dumps(response_changed),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.result_url)
        self.assertEqual(response.status_code, 200)
