from django.http import HttpResponse


def auto(req):
    return HttpResponse("auto page")