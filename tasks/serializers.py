from django.contrib.auth.models import User, Group
from rest_framework import serializers
from tasks.models import Task, History

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'users']
    def create(self, validated_data):
        print(validated_data)
        return Task.objects.create(**validated_data)
        History.objects.create(task_id=obj.id,action=0)   
        return obj


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['task_id', 'date', 'action', 'title', 'description', 'status', 'users']

class HistoryPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['task_id', 'title', 'description', 'status', 'users']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']