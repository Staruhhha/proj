from django.shortcuts import render
from django.http import HttpResponse
import datetime


def test_method(request):
    now = datetime.datetime.now()
    html = "<html><body>Текущее время %s</body></html>" %now
    return HttpResponse(html)