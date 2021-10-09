from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Disease, Question, Category, SurveyResponse, Result
from .serializers import (DiseaseSerializer, QuestionSerializer,
                          CategorySerializer, SurveyResponseSerializer,
                          ResultSerializer)
from .analysis import worker


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
        # TODO: invoke analyzers
        worker(session_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
            # TODO: check if it is in queue
            pass
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)
