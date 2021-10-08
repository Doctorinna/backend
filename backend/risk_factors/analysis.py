import pandas as pd

from .models import Question, SurveyResponse


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
    print(f"\nAttributes for model:\n{attributes}")
    print(f"Response of user:\n {df}")
    df.to_csv('response.csv')
    return df
