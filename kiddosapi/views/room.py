"""View module for handling requests about room"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import serializers, status
from kiddosapi.models import Room, Kid, FaveRoom


class RoomView(ViewSet):
    """Kiddos room view"""
    permission_classes = [ DjangoModelPermissions ]
    queryset = Room.objects.none()

    def retrieve(self, request, pk):
        """Handle GET requests for single room 
        
        Returns:
            Response -- JSON serialized room 
        """
        try:
            room = Room.objects.get(pk=pk)
            serializer = RoomSerializer(room)
            return Response(serializer.data)
        except Room.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    def list(self, request):
        """Handle GET requests to get all room 

        Returns:
            Response -- JSON serialized list of room
        """
        rooms = Room.objects.all()
        kid = Kid.objects.get(user=request.auth.user)
        for room in rooms:
            # Check to see if the room is in the attendees list on the room
            room.faved = kid in room.fave_rooms.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized room instance
        """
        parent = request.auth.user
        try:
            serializer = CreateRoomSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(parent=parent)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests for a room

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            room = Room.objects.get(pk=pk)
            serializer = CreateRoomSerializer(room, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk):
        room = Room.objects.get(pk=pk)
        room.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
    @action(methods=['put'], detail=True)
    def fave_room(self, request, pk):
        """Put for a kid to favorite a room"""
        kid = Kid.objects.get(user=request.auth.user)
        room = Room.objects.get(pk=pk)
        room.fave_rooms.add(kid)
        room.save()
        return Response({'message': 'Room faved'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['put'], detail=True)
    def unfave_room(self, request, pk):
        """Put for a kid to unfave a room"""
        kid = Kid.objects.get(user=request.auth.user)
        room = Room.objects.get(pk=pk)
        room.fave_rooms.remove(kid)
        return Response({'message': 'Room unfaved'}, status=status.HTTP_204_NO_CONTENT)
    
class RoomSerializer(serializers.ModelSerializer):
    """JSON serializer for room
    """
    class Meta:
        model = Room
        fields = ('id', 'name', 'parent', 'fave_rooms', 'faved')
        
class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name']