from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils.translation import ugettext
from django.conf import settings

def index(req,):
    LANGUAGE_code = req.GET.get('languageb')
    if LANGUAGE_code:
        LANGUAGE_CODE = LANGUAGE_code
    else:
        LANGUAGE_CODE = req.LANGUAGE_CODE
    context = { 'language_code': LANGUAGE_CODE,
                'LANGUAGES': settings.LANGUAGES,}
    tem = 'index.html'
    return render_to_response(tem, context)
