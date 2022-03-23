from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from kiddosapi.models import Kid


class KidView(ViewSet):

    def retrieve(self, request, pk):
        try:
            kid = Kid.objects.get(pk=pk)
            serializer = KidSerializer(kid)
            return Response(serializer.data)
        except Kid.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        kids = Kid.objects.all()
        kids = Kid.objects.order_by('-user__username')
        serializer = KidSerializer(kids, many=True)
        return Response(serializer.data)

class KidSerializer(serializers.ModelSerializer):
    """JSON serializer for kid
    """

    class Meta:
        model = Kid
        fields = ('id', 'user', 'age', 'parent')
        depth = 1

