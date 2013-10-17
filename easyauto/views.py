#from django.conf import settings
#from django.http import HttpResponse
from django.shortcuts import render_to_response


def auto(req):
    tem = "auto.html"
    return render_to_response(tem, {})


def ryan(req):
    tem = "ryan.html"
    return render_to_response(tem, {})
