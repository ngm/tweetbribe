from django.template import Context, loader
from django.http import HttpResponse

def index(request):
    t = loader.get_template('home/index.html')
    c = Context({
    })
    return HttpResponse(t.render(c))

def another(request):
    t = loader.get_template('home/another_page.html')
    c = Context({
    })
    return HttpResponse(t.render(c))