from django.contrib.auth.models import User
from tasks.models import Task, History, REMOVED
from rest_framework import viewsets, permissions,  mixins,  status
from tasks.serializers import UserSerializer, TaskSerializer, HistorySerializer, HistoryPointSerializer
from rest_framework.response import Response
from django.http import Http404
from datetime import datetime
from tasks.permissions import UserPermsDecorator

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed or edited.
    """
    
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def filter_queryset(self, queryset):
        try:
            queryset = queryset.all()
            title = self.request.query_params.get('title')
            if title is not None: 
                queryset =  queryset.filter(title__iexact=title)
            description = self.request.query_params.get('description')
            if description is not None: 
                queryset = queryset.filter(description__icontains=description)
            status = self.request.query_params.get('status')
            if status is not None: 
                queryset = queryset.filter(status__iexact=status)
            users = self.request.query_params.get('users')
            if users is not None: 
                queryset = queryset.filter(users__id__icontains=users)
        except:
            raise Http404
        return super().filter_queryset(queryset)
    
    def destroy(self, request, pk=None):
        instance = self.queryset.get(pk=pk)       
        data= instance.__dict__
        data.update({'task_id':instance.id,'action':REMOVED})
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
    def filter_queryset(self, queryset):
        try:
            queryset = queryset.all()
            id = self.request.query_params.get('id')
            if id is not None: 
                queryset = queryset.filter(task_id__iexact=id)
            action = self.request.query_params.get('action')
            if action is not None: 
                queryset = queryset.filter(action__iexact=action)
            when = self.request.query_params.get('when')
            if when is not None: 
                queryset = queryset.filter(date__lte=datetime.fromtimestamp(int(when))).order_by('task_id','-date').distinct('task_id').exclude(action=REMOVED)
        except:
            raise Http404
        return super().filter_queryset(queryset)
    
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    @UserPermsDecorator
    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True,context={'request': request})
        return Response(serializer.data)