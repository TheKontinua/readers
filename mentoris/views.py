from django.http import HttpResponse
from django.template import loader


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