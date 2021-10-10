from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import pickle
import os
import warnings
from .utils import (diabetes_format, cardio_format, stroke_format)
from backend.settings import BASE_DIR

warnings.filterwarnings('ignore')


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
