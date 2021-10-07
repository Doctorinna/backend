import pandas as pd

from .models import Question, SurveyResponse


def get_attributes(session_id):
    columns, values = [], []
    responses = SurveyResponse.objects.filter(session_id=session_id)
    for response in responses:
        question = Question.objects.get(pk=response.question_id)
        columns.append(question.label)
        values.append(response.answer)
    df = pd.DataFrame([values], columns=columns)
    df = df.apply(pd.to_numeric, errors='ignore')
    return df
