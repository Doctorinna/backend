from rest_framework import permissions, status
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
