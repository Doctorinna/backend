from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Disease, Question, Category
from .serializers import (DiseaseSerializer, QuestionSerializer,
                          CategorySerializer)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def diseases_list(request):
    # view responding to GET request by sending serialized disease objects
    if request.method == 'GET':
        snippets = Disease.objects.all()
        serializer = DiseaseSerializer(snippets, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def questions_list(request):
    # view responding to GET request by sending serialized question objects
    if request.method == 'GET':
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def categories_list(request):
    # view responding to GET request by sending serialized categories objects
    if request.method == 'GET':
        questions = Category.objects.all()
        serializer = CategorySerializer(questions, many=True)
        return Response(serializer.data)
