from django.db import models

# Create your models here.
class WebSearch(models.Model):
    user_search = models.CharField(max_length=150)
    exa_result = models.JSONField(default=list)
    wikipedia_result = models.JSONField(default=list)
    duckduckgo_result = models.JSONField(default=list)

    def __str__(self):
        return self.filename