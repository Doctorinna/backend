import random
from .test_setup import TestSetUp
from risk_factors.models import (Disease, Category, Range, Question, Option,
                                 SurveyResponse)


class TestDisease(TestSetUp):
    def test_disease_to_string(self):
        diseases = list(Disease.objects.all())
        disease = random.choice(diseases)
        self.assertEqual(str(disease), disease.illness)


class TestCategory(TestSetUp):
    def test_category_to_string(self):
        categories = list(Category.objects.all())
        category = random.choice(categories)
        self.assertEqual(str(category), category.title)


class TestRange(TestSetUp):
    def test_range_to_string(self):
        ranges = list(Range.objects.all())
        range_obj = random.choice(ranges)
        self.assertEqual(str(range_obj), f"[{range_obj.min}..{range_obj.max}]")


class TestOption(TestSetUp):
    def test_option_to_string(self):
        options = list(Option.objects.all())
        option = random.choice(options)
        self.assertEqual(str(option), option.answer)


class TestQuestion(TestSetUp):
    def test_question_to_string(self):
        questions = list(Question.objects.all())
        question = random.choice(questions)
        self.assertEqual(str(question), question.description)


class TestSurveyResponse(TestSetUp):
    def test_survey_response_to_string(self):
        survey_responses = list(SurveyResponse.objects.all())
        survey_response = random.choice(survey_responses)
        true_output = f"{survey_response.question} - {survey_response.answer}"
        self.assertEqual(str(survey_response), true_output)
