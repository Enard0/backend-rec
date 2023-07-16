from django.contrib.auth.models import User, Group
from tasks.models import Task
from rest_framework import viewsets, permissions
from tasks.serializers import UserSerializer, GroupSerializer, TaskSerializer
from rest_framework.response import Response

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed or edited.
    """
    
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    def list(self, request):
        queryset = Task.objects.all()
        title = request.query_params.get('title')
        if title!=None: queryset =  queryset.filter(title__iexact=title)
        description = request.query_params.get('description')
        if description!=None: queryset = queryset.filter(description__icontains=description)
        status = request.query_params.get('status')
        if status!=None: queryset = queryset.filter(status__iexact=status)
        users = request.query_params.get('users')
        if users!=None: queryset = queryset.filter(users__id__icontains=users)
        serializer = TaskSerializer(queryset, many=True,context={'request': request})
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]