"""View module for handling requests about game"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import serializers, status
from kiddosapi.models import MeetUp, Kid


class MeetUpView(ViewSet):
    """Kiddos meetUp view"""
    permission_classes = [ DjangoModelPermissions ]
    queryset = MeetUp.objects.none()

    def retrieve(self, request, pk):
        """Handle GET requests for single meet up 
        
        Returns:
            Response -- JSON serialized meet up 
        """
        try:
            meet_up = MeetUp.objects.get(pk=pk)
            serializer = MeetUpSerializer(meet_up)
            return Response(serializer.data)
        except MeetUp.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    def list(self, request):
        """Handle GET requests to get all meet ups 

        Returns:
            Response -- JSON serialized list of meet ups
        """
        meet_ups = MeetUp.objects.all()
        serializer = MeetUpSerializer(meet_ups, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        kid = Kid.objects.get(user=request.auth.user)
        try:
            serializer = CreateMeetUpSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(kid=kid)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            meet_up = MeetUp.objects.get(pk=pk)
            serializer = CreateMeetUpSerializer(meet_up, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk):
        meet_up = MeetUp.objects.get(pk=pk)
        meet_up.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
    
class MeetUpSerializer(serializers.ModelSerializer):
    """JSON serializer for meet up
    """
    class Meta:
        model = MeetUp
        fields = ('id', 'game', 'kid', 'approved', 'game_system', 'date', 'room')
        depth = 1
        
class CreateMeetUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetUp
        fields = ['id', 'game', 'game_system', 'room']