from django.http import HttpResponse

def auto(req):
    tem = "<title>auto</title><H1>test of h1</h1>"
    return HttpResponse(tem)
