from django.db import models


class brand(models.Model):
    brandname = models.CharField(max_length=30)
    nation = models.CharField(max_length=30)
    history = models.TextField(null=True, blank=True)
    creattime = models.DateTimeField(auto_now_add=True)
