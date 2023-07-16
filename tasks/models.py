from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

STATUS_CHOICES = ((0,'Nowy'),(1,'W toku'), (2,'Rozwiązany'))

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

