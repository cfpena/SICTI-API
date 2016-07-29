from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from tokenapi.decorators import token_required
from tokenapi.http import JsonResponse, JsonError
from .serializers import UserSerializer, GroupSerializer

@token_required
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

@token_required
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
# Create your views here.
