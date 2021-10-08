from faker import Faker
import random
from rest_framework.test import APITestCase
from django.urls import reverse

from risk_factors.models import Disease, Category, Range, Question, Option


class TestSetUp(APITestCase):
    def setUp(self):
        self.diseases_url = reverse('diseases')
        self.categories_url = reverse('categories')
        self.questions_url = reverse('questions')

        self.categories_used = []

        self.faker = Faker()
        num_obj = (1, 10)

        num_diseases = random.randint(*num_obj)
        for _ in range(num_diseases):
            diseases_all = list(Disease.objects.all())
            illnesses = [d.illness for d in diseases_all]
            illness = self.faker.word()
            while illness in illnesses:
                illness = self.faker.word()

            Disease.objects.create(illness=illness,
                                   description=self.faker.sentence())

        num_categories = random.randint(*num_obj)
        for _ in range(num_categories):
            categories_all = list(Category.objects.all())
            categories_titles = [c.title for c in categories_all]
            category_title = self.faker.word()
            while category_title in categories_titles:
                category_title = self.faker.word()
            Category.objects.create(title=category_title)

        num_ranges = random.randint(*num_obj)
        for _ in range(num_ranges):
            Range.objects.create(min=self.faker.random_int(),
                                 max=self.faker.random_int())

        diseases_all = list(Disease.objects.all())
        connected_diseases_num = random.randint(0, len(diseases_all))
        questions_num = random.randint(*num_obj)
        answers_total = 0
        for _ in range(questions_num):
            categories = list(Category.objects.all())
            ranges = list(Range.objects.all())

            random_category = random.choice(categories)
            self.categories_used.append(random_category)
            question_create_args = {
                'description': self.faker.text(),
                'label': self.faker.word(),
                'category_id': random_category.id,
            }
            threshold_range_creation = 0.5
            if random.random() > threshold_range_creation:
                random_range = random.choice(ranges)
                question_create_args['range_id'] = random_range.id

            question_obj = Question.objects.create(**question_create_args)
            for idx in range(connected_diseases_num):
                question_obj.diseases.add(diseases_all[idx - 1])

            answers_num = random.randint(*num_obj)
            answers_total += answers_num
            for _ in range(answers_num):
                Option.objects.create(question_id=question_obj.id,
                                      answer=self.faker.word)
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
