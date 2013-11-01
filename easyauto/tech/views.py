from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.utils import timezone

from tech.models import TechKind, TechBlog, BlogComment


def tech(req):
    cont = {}
    kinds = TechKind.objects.all()
    blogs = TechBlog.objects.all()
    comms = BlogComment.objects.all()
    if kinds:
        cont.update({'kinds': kinds})
    if blogs:
        cont.update({'blogs': blogs})
    cont.update({'timezone': timezone})
    tem = 'tech.html'
    return render_to_response(tem, cont)


def julia(req):
    tem = 'julia_learning.html'
    cont = {}
    julia = TechKind.objects.get(kind_name="Julia")
    blogs = TechBlog.objects.filter(kind=julia)
    cont.update({
                "julia": julia,
                "blogs": blogs,
                })
    return render_to_response(tem, cont)
