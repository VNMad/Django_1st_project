from django.http import HttpResponse
from django.shortcuts import render

def main_menu(request):
    return HttpResponse("<h1>Hello, V_NMad</h1>")