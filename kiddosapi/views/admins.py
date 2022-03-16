"""View module for handling requests about game"""
from crypt import methods
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import serializers, status
from kiddosapi.models import Game, Kid, Room, MeetUp
from django.contrib.auth.models import User


class AdminView(ViewSet):
    """Kiddos game view"""
    permission_classes = [ DjangoModelPermissions ]
    queryset = Game.objects.none()

    @action(methods=['get'], detail=False)
    def listofgames(self, request):
        """Get request for parents to get a list of everything at once"""
        
        parent = request.auth.user
        if parent.is_staff:
            kids = Kid.objects.filter(parent_id=parent.id)
            games = Game.objects.filter(kid__in=kids)
            serializer = GameSerializer(games, many=True)
            return Response(serializer.data)
        
    @action(methods=['get'], detail=False)
    def listofrooms(self, request):
        """Get request for parents to get a list of everything at once"""
        
        parent = request.auth.user
        if parent.is_staff:
            rooms = Room.objects.filter(parent_id=parent.id)
            serializer = RoomSerializer(rooms, many=True)
            return Response(serializer.data)
        
    @action(methods=['get'], detail=False)
    def listofmeetups(self, request):
        """Get request for parents to get a list of everything at once"""
        
        parent = request.auth.user
        if parent.is_staff:
            kids = Kid.objects.filter(parent_id=parent.id)
            meet_ups = MeetUp.objects.filter(kid__in=kids)
            serializer = MeetUpSerializer(meet_ups, many=True)
            return Response(serializer.data)
        
    
    
class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game
    """
    class Meta:
        model = Game
        fields = ('id', 'name', 'kid', 'approved', 'min_age')
        depth = 2
        
class RoomSerializer(serializers.ModelSerializer):
    """JSON serializer for room
    """
    class Meta:
        model = Room
        fields = ('id', 'name', 'parent')
        
class MeetUpSerializer(serializers.ModelSerializer):
    """JSON serializer for meet up
    """
    class Meta:
        model = MeetUp
        fields = ('id', 'game', 'kid', 'approved', 'game_system', 'date', 'room')
        depth = 1