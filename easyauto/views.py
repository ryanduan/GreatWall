#from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils.translation import get_language
from django.utils.translation import ugettext as _


def ryan(request):
    return HttpResponse("Hello world")
