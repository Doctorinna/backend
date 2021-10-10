from .utils import (get_prescription, get_attributes, get_group)
from .models import Disease, Result, Score, Question, SurveyResponse
from .analysis import cardio_risk_group, diabetes_risk_group, stroke_risk_group
from statistics import mean
from celery import shared_task


@shared_task
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
        session_id=session_id,
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
