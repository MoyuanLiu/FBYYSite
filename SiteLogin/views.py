from django.shortcuts import render
from django.template import loader

# Create your views here.
def login(request):
    t = loader.get_template('login.html')
    return t.render_to_response()
