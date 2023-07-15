from django.db import models
from django.conf import Settings

from django.contrib.auth.models import User

STATUS_CHOICES = ((0,'Nowy'),(1,'W toku'), (2,'Rozwiazany'))

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default="",blank=True)
    status = models.CharField(choices=STATUS_CHOICES, default='Nowy', max_length=100)
    user = models.ForeignKey(User,related_name='tasks',on_delete=models.CASCADE, null=True,default=None, blank=True)
    
    def save(self, *args, **kwargs):
        choice = self.status
        if not any(choice in _tuple for _tuple in STATUS_CHOICES):
            raise ValueError('Invalid value.')
        super(Task, self).save(*args, **kwargs)

