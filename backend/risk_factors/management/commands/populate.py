import pandas as pd
import os

from django.core.management.base import BaseCommand
from risk_factors.models import (Disease, Category, Question, Range, Option)
from backend.settings import BASE_DIR


def purge_objects():
    for model in [Disease, Category, Question, Range, Option]:
        model.objects.all().delete()


def populate_diseases(path):
    file_path = os.path.join(BASE_DIR, path)
    diseases_df = pd.read_csv(file_path)

    for _, row in diseases_df.iterrows():
        Disease.objects.create(illness=row['disease'],
                               description=row['description'])


def populate_questionnaire(questions_path, answers_path, mapping_path):
    questions_path = os.path.join(BASE_DIR, questions_path)
    options_dir = os.path.join(BASE_DIR, answers_path)
    mapping_path = os.path.join(BASE_DIR, mapping_path)

    questions_df = pd.read_csv(questions_path)
    mapping_df = pd.read_csv(mapping_path)
    for _, questions_row in questions_df.iterrows():
        attributes = ['id', 'category', 'min', 'max', 'question', 'label']
        (question_id_csv, category, range_min, range_max, description,
         label) = questions_row[attributes]

        category_obj, _ = Category.objects.get_or_create(title=category)
        question_create_args = {
            'description': description,
            'label': label,
            'category_id': category_obj.id
        }
        if not pd.isna(range_min) and not pd.isna(range_max):
            range_obj, _ = Range.objects.get_or_create(min=range_min,
                                                       max=range_max)
            question_create_args['range_id'] = range_obj.id
        question_obj = Question.objects.create(**question_create_args)

        question_mapping = mapping_df['question_id'] == question_id_csv
        mapped_diseases = mapping_df.loc[question_mapping]
        diseases_titles = mapped_diseases['disease_id']
        for diseases_title in diseases_titles:
            disease = Disease.objects.get(illness=diseases_title)
            question_obj.diseases.add(disease)

        options_path = os.path.join(options_dir, f'{question_id_csv}.csv')
        if os.path.exists(options_path):
            options_df = pd.read_csv(options_path)
            for _, options_row in options_df.iterrows():
                answer = options_row['answer']
                Option.objects.create(question_id=question_obj.id,
                                      answer=answer)


class Command(BaseCommand):
    help = 'Populates database with disease data.'

    def handle(self, *args, **options):
        purge_objects()

        entities = {
            'diseases': {
                'path': ['risk_factors/management/commands/data/diseases.csv'],
                'method': populate_diseases,
                'models': ['Disease']

            },
            'questionnaire': {
                'path': ['risk_factors/management/commands/data/questions.csv',
                         'risk_factors/management/commands/data/options/',
                         'risk_factors/management/commands/data/mapping.csv'],
                'method': populate_questionnaire,
                'models': ['Question', 'Option', 'Range', 'Category']
            },
        }

        models_populated = []
        for entity, metadata in entities.items():
            message = f"  Populating {entity} objects..."
            self.stdout.write(message, ending=' ')
            metadata['method'](*metadata['path'])
            models_populated += metadata['models']
            self.stdout.write(self.style.SUCCESS('OK'))
            self.stdout.flush()
        models_populated = ', '.join(models_populated)

        message = f"Successfully populated {models_populated} objects."
        self.stdout.write(self.style.SUCCESS(message))
        self.stdout.flush()
