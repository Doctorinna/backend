from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Disease
from .serializers import DiseaseSerializer


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def diseases_list(request):
    # view responding to GET request by sending serialized disease objects
    if request.method == 'GET':
        snippets = Disease.objects.all()
        serializer = DiseaseSerializer(snippets, many=True)
        return Response(serializer.data)
