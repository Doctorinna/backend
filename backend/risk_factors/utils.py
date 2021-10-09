import pandas as pd

from .models import Question, SurveyResponse


def replace(response, attributes):
    for attribute, mapping in attributes.items():
        response[attribute] = response[attribute].replace(*mapping)
    return response


def get_attributes(session_id):
    columns, values = [], []
    responses = SurveyResponse.objects.filter(session_id=session_id)
    attributes = {}
    for response in responses:
        question = Question.objects.get(pk=response.question_id)
        for disease in question.diseases.all():
            if disease.illness not in attributes:
                attributes[disease.illness] = []
            attributes[disease.illness].append(question.label)
        columns.append(question.label)
        values.append(response.answer)
    df = pd.DataFrame([values], columns=columns)
    df = df.apply(pd.to_numeric, errors='ignore')
    return df, attributes


def cardio_format(response):
    attributes_format = {
        'cholesterol': (['Normal', 'Above normal', 'Well above normal'],
                        [1, 2, 3]),
        'Gender': (['Female', 'Male'], [1, 2]),
        'gluc': (['Normal', 'Above normal', 'Well above normal'],
                 [1, 2, 3]),
        'smoke': (['No', 'Yes'], [0, 1]),
        'alco': (['No', 'Yes'], [0, 1]),
        'active': (['No', 'Yes'], [0, 1])
    }
    response = replace(response, attributes_format)
    return response


def diabetes_format(response):
    attributes_format = {
        'Gender': (['Male', 'Female'], [1, 2]),
        'Polyuria': (['Yes', 'No'], [0, 1]),
        'Polydipsia': (['Yes', 'No'], [0, 1]),
        'sudden weight loss': (['Yes', 'No'], [0, 1]),
        'visual blurring': (['Yes', 'No'], [0, 1]),
        'Itching': (['Yes', 'No'], [0, 1]),
        'weakness': (['Yes', 'No'], [0, 1]),
        'Polyphagia': (['Yes', 'No'], [0, 1]),
        'Irritability': (['Yes', 'No'], [0, 1]),
        'partial paresis': (['Yes', 'No'], [0, 1]),
        'Genital thrush': (['Yes', 'No'], [0, 1]),
        'delayed healing': (['Yes', 'No'], [0, 1]),
        'muscle stiffness': (['Yes', 'No'], [0, 1]),
        'Alopecia': (['Yes', 'No'], [0, 1]),
        'Obesity': (['Yes', 'No'], [0, 1])
    }
    replace(response, attributes_format)
    return response


def stroke_format(response, weight, height):
    attributes_format = {
        'Gender': (['Male', 'Female'], [1, 2]),
        'hypertension': (['No', 'Yes'], [0, 1]),
        'heart_disease': (['No', 'Yes'], [0, 1]),
        'smoking_status': (['Formerly smoked', 'Smokes', 'Never smoked',
                            'Unknown'], [4, 3, 2, 1]),
        'ever_married': (['No', 'Yes'], [0, 1]),
        'work_type': (['children', 'Never_worked', 'Self-employed', 'Private',
                       'Govt_job'], [1, 2, 3, 4, 5]),
        'avg_glucose_level': (['I don\'t know'], [106.15]),
        'Residence_type': (['Rural', 'Urban'], [1, 2]),
        'bmi': (['Compute from my height and weight'],
                [weight / (height ** 2)])

    }
    replace(response, attributes_format)
    return response


def get_prescription(score):
    if score < 0.2:
        return 'Your results indicate that you are at a low risk group ' \
               'of disease.'
    if score < 0.5:
        return 'Your results indicate that you are at a low risk group of ' \
               'disease. It is recommended to visit a doctor and take the ' \
               'medical check-up. You should follow an active and healthy ' \
               'lifestyle to improve your condition.'
    if score < 0.8:
        return 'Your results indicate that you are at a medium risk group ' \
               'of disease. It is necessary to visit a doctor and take the ' \
               'medical check-up. You should, based on your condition, ' \
               'adhere to an active and healthy lifestyle as possible ' \
               'to improve your condition.'
    return 'Your results indicate that you are at a high risk group of ' \
           'disease. It is vital to visit a doctor and take the medical ' \
           'check-up. Talk to your doctor before changing your lifestyle.'
