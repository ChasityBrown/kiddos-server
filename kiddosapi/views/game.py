"""View module for handling requests about game"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import serializers, status
from kiddosapi.models import Game, Kid, FaveGame


class GameView(ViewSet):
    """Kiddos game view"""
    permission_classes = [ DjangoModelPermissions ]
    queryset = Game.objects.none()

    def retrieve(self, request, pk):
        """Handle GET requests for single game 
        
        Returns:
            Response -- JSON serialized game 
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    def list(self, request):
        """Handle GET requests to get all game 

        Returns:
            Response -- JSON serialized list of game
        """
        user = User.objects.get(id=request.auth.user.id)
        if user.is_staff:
            games = Game.objects.all() 
            serializer = GameSerializer(games, many=True)
            return Response(serializer.data)
        else:
            games = Game.objects.all()
            kid = Kid.objects.get(user=request.auth.user)
            for game in games:
                # Check to see if the gamer is in the attendees list on the game
                game.faved = kid in game.fave_games.all()
            serializer = GameSerializer(games, many=True)     
            return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        kid = Kid.objects.get(user=request.auth.user)
        try:
            serializer = CreateGameSerializer(data=request.data)
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
        parent = Kid.objects.get(user=request.auth.user)
        try:
            game = Game.objects.get(pk=pk)
            serializer = CreateGameSerializer(game, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(parent=parent)
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
    @action(methods=['post'], detail=True)
    def fave_game(self, request, pk):
        """Post for a kid to favorite a game"""
        kid = Kid.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=pk)
        game.fave_games.add(kid)
        game.save()
        return Response({'message': 'Game faved'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=True)
    def unfave_game(self, request, pk):
        """Delete for a kid to unfave a game a game"""
        kid = Kid.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=pk)
        game.fave_games.remove(kid)
        return Response({'message': 'Game unfaved'}, status=status.HTTP_204_NO_CONTENT)
class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game
    """
    class Meta:
        model = Game
        fields = ('id', 'name', 'kid', 'approved', 'min_age', 'fave_games', 'faved')
        depth = 2
        
class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'name']