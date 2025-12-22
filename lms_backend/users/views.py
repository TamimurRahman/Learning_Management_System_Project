from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import User
from . import serializers
# Create your views here.

@api_view(['GET','POST'])
def user_list_create(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return Response({'detail':'Authentication credentials where not provided'},status=status.HTTP_401_UNAUTHORIZED)
        
        if request.user.role == 'admin':
            users = User.objects.all()
        else:
            users = User.objects.filter(id=request.user.id)
        serializer = serializers.UserSerializer(users, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

