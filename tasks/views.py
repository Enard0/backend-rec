from django.contrib.auth.models import User, Group
from tasks.models import Task, History
from rest_framework import viewsets, permissions,  mixins,  status
from tasks.serializers import UserSerializer, GroupSerializer, TaskSerializer, HistorySerializer
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
        queryset = Task.objects.all()
        try:
            title = request.query_params.get('title')
            if title!=None: queryset =  queryset.filter(title__iexact=title)
            description = request.query_params.get('description')
            if description!=None: queryset = queryset.filter(description__icontains=description)
            status = request.query_params.get('status')
            if status!=None: queryset = queryset.filter(status__iexact=status)
            users = request.query_params.get('users')
            if users!=None: queryset = queryset.filter(users__id__icontains=users)
        except:
            raise Http404
        serializer = TaskSerializer(queryset, many=True,context={'request': request})
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        _mutable = request.data._mutable
        request.data._mutable = True
        request.data.update({'task_id':serializer.instance.id,'action':0})
        request.data._mutable = _mutable
        hserializer = HistorySerializer(data=request.data,context={'request': request})
        hserializer.is_valid(raise_exception=True)
        self.perform_create(hserializer)
        return Response({'status': 'success', 'pk': serializer.instance.pk})
    
    def update(self, request, pk=None, project_pk=None):
        instance = self.queryset.get(pk=pk)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        _mutable = request.data._mutable
        request.data._mutable = True
        request.data.update({'task_id':serializer.instance.id,'action':1})
        request.data._mutable = _mutable
        hserializer = HistorySerializer(data=request.data,context={'request': request})
        hserializer.is_valid(raise_exception=True)
        self.perform_create(hserializer)
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
        queryset = History.objects.all()
        try:
            id = request.query_params.get('id')
            if id!=None: queryset = queryset.filter(task_id__iexact=id)
            action = request.query_params.get('action')
            if action!=None: queryset = queryset.filter(action__iexact=status)
            when = request.query_params.get('when')
            if when!=None: queryset = [queryset.filter(date__lte=datetime.fromtimestamp(int(when))).latest('date')]
        except:
            raise Http404
        serializer = HistorySerializer(queryset, many=True,context={'request': request})
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