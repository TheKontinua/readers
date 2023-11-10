from django.http import HttpResponse
from django.template import loader
from mentapp.models import User
from django.shortcuts import render, get_object_or_404


def katex(request):
    template = loader.get_template("katex/index.html")
    return HttpResponse(template.render())


def login(request):
    template = loader.get_template("mentapp/login.html")
    return HttpResponse(template.render())


def sign_up(request):
    template = loader.get_template("mentapp/sign_up.html")
    return HttpResponse(template.render())

  
def profile(request):
    template = loader.get_template('mentapp/profile.html')
    return HttpResponse(template.render())

def user_info(request, user_id):
    user_profile = get_object_or_404(User, user_id=user_id)
    return render(request, 'mentapp/profile.html', {'user_profile': user_profile})