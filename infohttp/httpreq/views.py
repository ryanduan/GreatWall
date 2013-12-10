from django.shortcuts import render
from django.http import HttpResponse

def index(req):
    print req
    return HttpResponse("Hello")
