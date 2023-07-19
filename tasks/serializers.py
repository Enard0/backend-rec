from django.contrib.auth.models import User, Group
from rest_framework import serializers
from tasks.models import Task, History

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'users']

    def create(self, validated_data):
        usrs = validated_data.pop('users')
        obj = Task.objects.create(**validated_data)
        obj.users.set(usrs)
        validated_data.update({'task_id':obj.id,'action':0})
        his = History.objects.create(**validated_data)  
        his.users.set(usrs) 
        return obj
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        print(validated_data.get('users'))
        instance.users.set(validated_data.get('users', instance.users))
        instance.save()

        usrs = validated_data.pop('users')
        validated_data.update({'task_id':instance.id,'action':1})
        his = History.objects.create(**validated_data)  
        his.users.set(usrs)   
        return instance


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
        fields = ['url', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}