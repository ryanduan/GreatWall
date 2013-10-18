#from django.conf import settings
#from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils.translation import get_language


def auto(req):
    tem = "auto.html"
    return render_to_response(tem, {})


def ryan(request):
    context = {'language_code': get_language()[:2]}
    tem = "ryan.html"
    return render_to_response(tem, context)
