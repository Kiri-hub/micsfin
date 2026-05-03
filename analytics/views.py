from django.shortcuts import render
from  django.http.response import HttpResponse


def homepage(request):
    return HttpResponse('Helo world')