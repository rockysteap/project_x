from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Похоже страницу украли!</h1>')


def index(request):
    return render(request, 'dashboard/index.html')
