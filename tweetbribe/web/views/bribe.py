from django.template import Context, loader
from django.http import HttpResponse
from web.models import Charity

def index(request):
    t = loader.get_template('bribe/index.html')

    charities = []
    charities.append(Charity(name="Unicef", description="Cool dudes", givinglab_id="asdf", logo_url="http://asdf.com"))
    charities.append(Charity(name="Another", description="Cool dudes", givinglab_id="asdf", logo_url="http://asdf.com"))

    c = Context({
        "charities":charities
    })
    return HttpResponse(t.render(c))

