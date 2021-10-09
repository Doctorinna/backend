import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier

import os
from .utils import *
from .models import Disease, Result
from backend.settings import BASE_DIR
import warnings

warnings.filterwarnings('ignore')


def worker(session_id):
    df, attributes = get_attributes(session_id)
    diseases = list(Disease.objects.all())

    supported_methods = {
        'cardiovascular disease': cardio_risk_group,
        'diabetes': diabetes_risk_group,
        'stroke': stroke_risk_group
    }

    for disease in diseases:
        illness = disease.illness
        method = supported_methods[illness]
        score = method(df, attributes[illness])
        result = Result.objects.create(session_id=session_id,
                                       disease=disease,
                                       risk_factor=score[0],
                                       prescription=get_prescription(score))


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
