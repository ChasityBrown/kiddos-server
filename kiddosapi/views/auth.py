from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from kiddosapi.models import Kid

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a kid

    Method arguments:
      request -- The full HTTP request object
    '''
    username = request.data['username']
    password = request.data['password']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    authenticated_user = authenticate(username=username, password=password)

    # If authentication was successful, respond with their token
    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        data = {
            'valid': True,
            'token': token.key
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = { 'valid': False }
        return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new kid for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    if (request.data['parent']):
        parent_group = Group.objects.get(name="Parents")
        new_user = User.objects.create_user(
            username=request.data['username'],
            password=request.data['password'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            is_staff=True
        )
        new_user.groups.add(parent_group)
        token = Token.objects.create(user=new_user)
        # Return the token to the client
        data = { 'token': token.key }
        return Response(data)
        # Now save the extra info in the kiddosapi_kid table
    else:    
        kid_group = Group.objects.get(name="Kids")
        new_user = User.objects.create_user(
            username=request.data['username'],
            password=request.data['password'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name']
        )
        parent = User.objects.get(username=request.data['parent_username'])
        kid = Kid.objects.create(
            age=request.data['age'],
            user=new_user,
            parent=parent
        )
        new_user.groups.add(kid_group)
        # Use the REST Framework's token generator on the new user account
        token = Token.objects.create(user=kid.user)
        # Return the token to the client
        data = { 'token': token.key }
        return Response(data)
