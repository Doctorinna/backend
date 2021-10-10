import json

from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import HttpResponse
from django.db.models import Avg, Count

from .models import Disease, Question, Category, SurveyResponse, Result, Score
from .serializers import (DiseaseSerializer, QuestionSerializer,
                          CategorySerializer, SurveyResponseSerializer,
                          ResultSerializer)
from .tasks import worker
from .utils import THRESHOLDS


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def diseases_list(request):
    # view responding to GET request by sending serialized disease objects
    if request.method == 'GET':
        diseases = Disease.objects.all()
        serializer = DiseaseSerializer(diseases, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def categories_list(request):
    # view responding to GET request by sending serialized categories objects
    if request.method == 'GET':
        questions = Category.objects.all()
        serializer = CategorySerializer(questions, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def questions_list(request, category='__all__'):
    # view responding to GET request by sending serialized question objects
    if request.method == 'GET':
        category_objs = Category.objects.all()
        categories = [category.title for category in category_objs]

        if category in categories:
            questions = Question.objects.filter(category__title=category)
        elif category == '__all__':
            questions = Question.objects.all()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def submit_response(request):
    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key

    if request.method == 'GET':
        responses = SurveyResponse.objects.filter(session_id=session_id)
        serializer = SurveyResponseSerializer(responses, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SurveyResponseSerializer(data=request.data, many=True)

        if not serializer.is_valid():
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(serializer.errors, status=status_code)

        SurveyResponse.objects.filter(session_id=session_id).delete()
        for question_response in serializer.validated_data:
            response_create_kwargs = {
                'session_id': session_id,
                **question_response
            }
            SurveyResponse.objects.create(**response_create_kwargs)
        worker.delay(session_id)
        return Response(session_id, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes((permissions.AllowAny,))
def change_response(request, question):
    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key

    if request.method == 'PUT':
        serializer = SurveyResponseSerializer(data=request.data)

        if not serializer.is_valid():
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(serializer.errors, status=status_code)

        response = SurveyResponse.objects.get(session_id=session_id,
                                              question_id=question)
        response.answer = serializer.validated_data['answer']
        response.save()
        worker.delay(session_id)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_result(request, disease='__all__'):
    if request.method == 'GET':
        session_id = request.session.session_key
        diseases_obj = Disease.objects.all()
        diseases = [dis.illness for dis in diseases_obj]

        results = Result.objects.filter(session_id=session_id)
        if disease in diseases:
            results = results.filter(disease__illness=disease)
            if not results.exists():
                # TODO: check if it is in queue
                return Response(status=status.HTTP_202_ACCEPTED)
        elif disease == '__all__':
            if not results.exists():
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_result_session(request, session, disease='__all__'):
    if request.method == 'GET':
        session_id = session
        diseases_obj = Disease.objects.all()
        diseases = [dis.illness for dis in diseases_obj]

        results = Result.objects.filter(session_id=session_id)
        if disease in diseases:
            results = results.filter(disease__illness=disease)
            if not results.exists():
                # TODO: check if it is in queue
                return Response(status=status.HTTP_202_ACCEPTED)
        elif disease == '__all__':
            if not results.exists():
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_score(request):
    if request.method == 'GET':
        session_id = request.session.session_key
        score_obj = Score.objects.filter(session_id=session_id)

        if score_obj.exists():
            score = (score_obj[0]).score

            scores_worse = len(Score.objects.filter(score__lt=score))
            scores_all = len(Score.objects.all())
            scores_worse_percents = scores_worse / scores_all * 100

            thresholds = {}
            for threshold, label in THRESHOLDS:
                thresholds[label] = threshold

            message = {
                'score': score,
                'better_than': scores_worse_percents,
                'thresholds': thresholds
            }
            return HttpResponse(json.dumps(message),
                                content_type='application/json')
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_score_session(request, session):
    if request.method == 'GET':
        session_id = session
        score_obj = Score.objects.filter(session_id=session_id)

        if score_obj.exists():
            score = (score_obj[0]).score

            scores_worse = len(Score.objects.filter(score__lt=score))
            scores_all = len(Score.objects.all())
            scores_worse_percents = scores_worse / scores_all * 100

            thresholds = {}
            for threshold, label in THRESHOLDS:
                thresholds[label] = threshold

            message = {
                'score': score,
                'better_than': scores_worse_percents,
                'thresholds': thresholds
            }
            return HttpResponse(json.dumps(message),
                                content_type='application/json')
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_statistics(request, disease):
    if request.method == 'GET':
        session_id = request.session.session_key
        disease_obj = Disease.objects.filter(illness=disease)
        result_obj = Result.objects.filter(session_id=session_id,
                                           disease__illness=disease)

        if disease_obj.exists() and result_obj.exists():
            # TODO: if not specified merge to other
            results_for_disease = Result.objects.filter(
                disease__illness=disease)
            results_grouped = results_for_disease.values('region')
            regions_avg_factor = results_grouped.annotate(
                avg_factor=Avg('risk_factor'))
            avg_factors_sorted = regions_avg_factor.order_by('-avg_factor')
            avg_factors_json = list(avg_factors_sorted)

            message = {
                'country': avg_factors_json,
            }

            user_region = (result_obj[0]).region
            if user_region != 'It\'s private':
                results_in_region = Result.objects.filter(
                    disease__illness=disease,
                    region=user_region)
                results_grouped = results_in_region.values('label')
                labels_number = results_grouped.annotate(
                    count=Count('session'))
                labels_number_json = list(labels_number)
                message['your_region'] = labels_number_json

            return HttpResponse(json.dumps(message),
                                content_type='application/json')
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_statistics_session(request, session, disease):
    if request.method == 'GET':
        session_id = session
        disease_obj = Disease.objects.filter(illness=disease)
        result_obj = Result.objects.filter(session_id=session_id,
                                           disease__illness=disease)

        if disease_obj.exists() and result_obj.exists():
            # TODO: if not specified merge to other
            results_for_disease = Result.objects.filter(
                disease__illness=disease)
            results_grouped = results_for_disease.values('region')
            regions_avg_factor = results_grouped.annotate(
                avg_factor=Avg('risk_factor'))
            avg_factors_sorted = regions_avg_factor.order_by('-avg_factor')
            avg_factors_json = list(avg_factors_sorted)

            message = {
                'country': avg_factors_json,
            }

            user_region = (result_obj[0]).region
            if user_region != 'It\'s private':
                results_in_region = Result.objects.filter(
                    disease__illness=disease,
                    region=user_region)
                results_grouped = results_in_region.values('label')
                labels_number = results_grouped.annotate(
                    count=Count('session'))
                labels_number_json = list(labels_number)
                message['your_region'] = labels_number_json

            return HttpResponse(json.dumps(message),
                                content_type='application/json')
        return Response(status=status.HTTP_404_NOT_FOUND)
