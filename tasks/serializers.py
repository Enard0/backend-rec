from rest_framework import serializers
from tasks.models import Task, STATUS_CHOICES
from django.contrib.auth.models import User
 

class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Task.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'tasks']

class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(default='')
    status = serializers.CharField(default='Nowy', max_length=100)
    user = serializers.SerializerMethodField(default=None, required=False)

    def create(self, validated_data):
        """
        Create and return a new `Task` instance, given the validated data.
        """
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Task` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        if not any(instance.status in _tuple for _tuple in STATUS_CHOICES):
            raise ValueError('Invalid value.')
        instance.save()
        return instance
    
    def delete(self, pk):
        task = self.get_object(pk)
        task.delete()
                        
    def get_user(self, b):
        return b.user