# agent/models.py
from django.db import models

# Create your models here.
class Agent(models.Model):
    user_messages = models.JSONField(default=list)
    agent_messages = models.JSONField(default=list)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


