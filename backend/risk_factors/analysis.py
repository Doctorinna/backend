import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier

import os
from .utils import (get_prescription, get_attributes, diabetes_format,
                    cardio_format, stroke_format, get_group)
from .models import Disease, Result, Score, Question, SurveyResponse
from backend.settings import BASE_DIR
import warnings
from statistics import mean

warnings.filterwarnings('ignore')


def worker(session_id):
    df, attributes = get_attributes(session_id)
    diseases = list(Disease.objects.all())

    supported_methods = {
        'cardiovascular disease': cardio_risk_group,
        'diabetes': diabetes_risk_group,
        'stroke': stroke_risk_group
    }

    question_region = Question.objects.get(label='region')
    session_region = (list(SurveyResponse.objects.filter(
        question_id=question_region.id))[0]).answer

    results = []
    for disease in diseases:
        illness = disease.illness

        result_kwargs = {
            'session_id': session_id,
            'disease': disease,
            'region': session_region
        }

        if illness not in supported_methods:
            result_kwargs['risk_factor'] = 0
            result_kwargs['prescription'] = 'Method is currently not supported'
        else:
            method = supported_methods[illness]
            score = method(df, attributes[illness])
            result_kwargs['risk_factor'] = float(score)
            result_kwargs['label'] = get_group(score)
            result_kwargs['prescription'] = get_prescription(score)

        result_obj = Result.objects.update_or_create(
            session_id=session_id, disease=disease,
            defaults=result_kwargs
        )
        results.append(result_obj[0])
    score = (1 - mean([res.risk_factor for res in results])) * 100
    Score.objects.create(session_id=session_id, score=score)


def cardio_risk_group(response, cardio_columns):
    cardio_response = cardio_format(response[cardio_columns])

    f = RandomForestClassifier()
    path = os.path.join(BASE_DIR, 'risk_factors/inference/cardio_model')
    with open(path, 'rb') as f:
        rf = pickle.load(f)

    pred = rf.predict_proba(cardio_response)
    pred = pd.DataFrame(data=pred, columns=['0', '1'])['1']
    return pred.values


def diabetes_risk_group(response, diabetes_columns):
    diabetes_response = diabetes_format(response[diabetes_columns])

    f = RandomForestClassifier()
    path = os.path.join(BASE_DIR, 'risk_factors/inference/diabetes_model')
    with open(path, 'rb') as f:
        rf = pickle.load(f)

    pred = rf.predict_proba(diabetes_response)
    pred = pd.DataFrame(data=pred, columns=['0', '1'])['1']
    return pred.values


def stroke_risk_group(response, stroke_columns):
    stroke_response = stroke_format(response[stroke_columns],
                                    response['weight'], response['height'])

    f = RandomForestClassifier()
    path = os.path.join(BASE_DIR, 'risk_factors/inference/stroke_model')
    with open(path, 'rb') as f:
        rf = pickle.load(f)

    pred = rf.predict_proba(stroke_response)
    pred = pd.DataFrame(data=pred, columns=['0', '1'])['1']
    return pred.values
