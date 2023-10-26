from django.http import HttpResponse
from django.template import loader

def katex(request):
    template = loader.get_template('katex/index.html')
    return HttpResponse(template.render())