from django.contrib.auth.models import User, Group
from tasks.models import Task, History
from rest_framework import viewsets, permissions,  mixins,  status
from tasks.serializers import UserSerializer, GroupSerializer, TaskSerializer, HistorySerializer, HistoryPointSerializer
from rest_framework.response import Response
from django.http import Http404
from datetime import datetime

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed or edited.
    """
    
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    def list(self, request):
        try:
            self.queryset = self.queryset.all()
            title = request.query_params.get('title')
            if title is not None: self.queryset =  self.queryset.filter(title__iexact=title)
            description = request.query_params.get('description')
            if description is not None: self.queryset = self.queryset.filter(description__icontains=description)
            status = request.query_params.get('status')
            if status is not None: self.queryset = self.queryset.filter(status__iexact=status)
            users = request.query_params.get('users')
            if users is not None: self.queryset = self.queryset.filter(users__id__icontains=users)
        except:
            raise Http404
        serializer = TaskSerializer(self.queryset, many=True,context={'request': request})
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        instance = self.queryset.get(pk=pk)       
        data= instance.__dict__
        data.update({'task_id':instance.id,'action':2})
        hserializer = HistorySerializer(data=data,context={'request': request})
        hserializer.is_valid(raise_exception=True)
        self.perform_create(hserializer)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class HistoryViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    API endpoint that allows history to be viewed.
    """
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    def list(self, request):
        try:
            id = request.query_params.get('id')
            if id is not None: self.queryset = self.queryset.filter(task_id__iexact=id)
            action = request.query_params.get('action')
            if action is not None: self.queryset = self.queryset.filter(action__iexact=status)
            when = request.query_params.get('when')
            if when is not None: self.queryset = [self.queryset.filter(date__lte=datetime.fromtimestamp(int(when))).latest('date')]
        except:
            raise Http404
        if when is None:
            serializer = HistorySerializer(self.queryset.order_by('date'), many=True,context={'request': request})
        else: 
            serializer = HistoryPointSerializer(self.queryset, many=True,context={'request': request})
            print(self.queryset[0].action)
            if self.queryset[0].action=='2':
                raise Http404                      
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