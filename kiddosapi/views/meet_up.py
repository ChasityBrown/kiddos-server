"""View module for handling requests about game"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.decorators import action
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
        user = User.objects.get(id=request.auth.user.id)
        if user.is_staff:
            meet_ups = MeetUp.objects.all() 
            serializer = MeetUpSerializer(meet_ups, many=True)
            return Response(serializer.data)
        else:
            meet_ups = MeetUp.objects.all()
            game = request.query_params.get('game', None)
            kid = Kid.objects.get(user=request.auth.user)
            if game is not None:
                meet_ups = meet_ups.filter(game_id=game)
            # Set the `joined` property on every meet_up
            for meet_up in meet_ups:
                # Check to see if the kid is in the attendees list on the meet_up
                meet_up.joined = kid in meet_up.attendees.all()
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
    
    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""
    
        kid = Kid.objects.get(user=request.auth.user)
        meet_up = MeetUp.objects.get(pk=pk)
        meet_up.attendees.add(kid) #Adds row to meet_up_kid join table when kid joins meet_up
        return Response({'message': 'Kid added'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['put'], detail=True)
    def leave(self, request, pk):
        """Post request for a user to sign up for an meet_up"""
    
        kid = Kid.objects.get(user=request.auth.user)
        meet_up = MeetUp.objects.get(pk=pk)
        meet_up.attendees.remove(kid)
        return Response({'message': 'Kid removed'}, status=status.HTTP_204_NO_CONTENT)
        
    
class MeetUpSerializer(serializers.ModelSerializer):
    """JSON serializer for meet up
    """
    class Meta:
        model = MeetUp
        fields = ('id', 'game', 'kid', 'approved', 'game_system', 'date', 'room', 'attendees', 'joined')
        depth = 1
        
class CreateMeetUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetUp
        fields = ['id', 'game', 'game_system', 'room']