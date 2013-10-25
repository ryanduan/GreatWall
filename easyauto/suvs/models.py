from django.db import models


class brand(models.Model):

    def __unicode__(self):
        return self.brandname

    brandname = models.CharField(max_length=30)
    nation = models.CharField(max_length=30)
    history = models.TextField(null=True, blank=True)
    phoneno_s = models.CharField(max_length=20, null=True, blank=True)
    phoneno_a = models.CharField(max_length=20, null=True, blank=True)
    creattime = models.DateTimeField(auto_now_add=True)


class serie(models.Model):

    def __unicode__(self):
        return self.seriesname

    brand = models.ForeignKey(brand)
    seriesname = models.CharField(max_length=30)
    engine = models.CharField(max_length=30, null=True, blank=True)
    displacement = models.CharField(max_length=20, null=True, blank=True)
    width = models.CharField(max_length=10, null=True, blank=True)
    length = models.CharField(max_length=10, null=True, blank=True)
    height = models.CharField(max_length=10, null=True, blank=True)
    wheelbase = models.CharField(max_length=10, null=True, blank=True)
    seatno = models.IntegerField(null=True, blank=True)
    speed = models.CharField(max_length=10, null=True, blank=True)
    price = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    creattime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(null=True, blank=True)
    stars = models.SmallIntegerField(null=True, blank=True)
    hot = models.SmallIntegerField(null=True, blank=True)
