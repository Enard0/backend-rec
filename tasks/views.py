from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from tasks.serializers import TaskSerializer, UserSerializer
from tasks.models import Task
from rest_framework.response import Response

# Create your views here.
class TaskView(viewsets.ViewSet):
    def list(self, request):
        print(request)
        queryset = Task.objects.all()
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

