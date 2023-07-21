from django.contrib.auth.models import User
from tasks.models import Task, History, REMOVED
from rest_framework import viewsets, permissions,  mixins,  status
from tasks.serializers import UserSerializer, TaskSerializer, HistorySerializer
from rest_framework.response import Response
from django.http import Http404
from django.core.exceptions import BadRequest
from datetime import datetime
from tasks.permissions import RegisterPerms, UserPerms

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
        except:
            raise Http404
        try:
            action = self.request.query_params.get('action')
            if action is not None: 
                queryset = queryset.filter(action__iexact=action)
        except:
            raise Http404    
        when = self.request.query_params.get('when')
        if when is not None: 
            if when.isnumeric():
                time = datetime.fromtimestamp(int(when))
            else:
                try:
                    time=datetime.fromisoformat(when.replace('Z',''))
                except:
                    raise BadRequest
            try:    
                queryset = queryset.filter(date__lte=time).order_by('task_id','-date').distinct('task_id').exclude(action=REMOVED)
            except:
                raise Http404
        return super().filter_queryset(queryset)
    
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [UserPerms]
    
class RegisterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = []
    serializer_class = UserSerializer
    permission_classes = [RegisterPerms]