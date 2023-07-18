from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

STATUS_CHOICES = ((0,'Nowy'),(1,'W toku'), (2,'Rozwiązany'))
ACTION_CHOICES = ((0,'Creation'),(1,'Edit'), (2,'Removal'))

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default="",blank=True)
    status = models.CharField(choices=STATUS_CHOICES, default='Nowy', max_length=100)
    users = models.ManyToManyField(
        User,
        verbose_name=_("users"),
        blank=True,
        help_text=_(
            "The users this task belongs to."
        ),
        related_name="user_set",
        related_query_name="user",
    )

    def save(self, *args, **kwargs):
        choice = self.status
        if not any(choice in _tuple for _tuple in STATUS_CHOICES):
            raise ValueError('Invalid value.')
        super(Task, self).save(*args, **kwargs)



class History(models.Model):
    task_id = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    description = models.TextField(default="",blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    users = models.ManyToManyField(
        User,
        blank=True,
        help_text=_(
            "The users this task belongs to."
        ),
        related_name="history_set",
        related_query_name="history",
    )
    date = models.DateTimeField(auto_now_add=True)
    action = models.IntegerField(choices=ACTION_CHOICES, default=0)