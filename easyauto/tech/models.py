from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class TechKind(models.Model):
    user = models.ForeignKey(User)
    kind_name = models.CharField(max_length=30)
    create_at = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.kind_name


class TechBlog(models.Model):
    kind = models.ForeignKey(TechKind)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=40)
    create_at = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    check_time = models.IntegerField(default=0)
    review_time = models.IntegerField(default=0)
    good_heart = models.SmallIntegerField(default=0)

    def __unicode__(self):
        return 'Blog: %s-%s-%s' % (self.title, self.kind, self.user)


class BlogComment(models.Model):
    blog = models.ForeignKey(TechBlog)
    user = models.ForeignKey(User)
    content = models.CharField(max_length=200)
    create_at = models.DateTimeField(default=timezone.now)
    good_heart = models.SmallIntegerField(default=0, blank=True)

    def __unicode__(self):
        return 'Comment: %s-%s' % (self.blog, self.user)
