from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from tech.models import TechKind, TechBlog, BlogComment


def tech(req):
    context = {}
    kinds = TechKind.objects.all()
    blogs = TechBlog.objects.all()
    comms = BlogComment.objects.all()
    if kinds:
        context.update({'kinds': kinds})
    if blogs:
        context.update({'blogs': blogs})
    tem = 'tech.html'
    return render_to_response(tem, context)
