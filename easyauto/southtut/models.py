from django.db import models
from django.utils import timezone


class GreatWall(models.Model):
    name = models.CharField(max_length=100)
    create_at = models.DateTimeField(default=timezone.now)
    deep_learning = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name

