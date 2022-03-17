"""View module for handling requests about room"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import serializers, status
from kiddosapi.models import Room, Kid, GameSystem


class GameSystemView(ViewSet):
    """Kiddos gameSystem view"""
    permission_classes = [ DjangoModelPermissions ]
    queryset = GameSystem.objects.none()

    def retrieve(self, request, pk):
        """Handle GET requests for single room 
        
        Returns:
            Response -- JSON serialized room 
        """
        try:
            game_system = GameSystem.objects.get(pk=pk)
            serializer = GameSystemSerializer(game_system)
            return Response(serializer.data)
        except GameSystem.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    def list(self, request):
        """Handle GET requests to get all game systems 

        Returns:
            Response -- JSON serialized list of game systems
        """
        game_systems = GameSystem.objects.all()
        serializer = GameSystemSerializer(game_systems, many=True)
        return Response(serializer.data)
   
class GameSystemSerializer(serializers.ModelSerializer):
    """JSON serializer for gameSystem
    """
    class Meta:
        model = GameSystem
        fields = ('id', 'name')
        