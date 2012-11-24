from django.template import Context, loader
from django.http import HttpResponse
from web.models import Charity, Bribe
from django.shortcuts import redirect

def index(request):
    t = loader.get_template('bribe/index.html')

    charities = []
    charities.append(Charity(name="Unicef", description="Cool dudes", givinglab_id="asdf", logo_url="http://asdf.com"))
    charities.append(Charity(name="Another", description="Cool dudes", givinglab_id="asdf", logo_url="http://asdf.com"))

    c = Context({
        "charities":charities
    })
    return HttpResponse(t.render(c))


def view(request, bribe_id):
    t = loader.get_template('bribe/view.html')

    bribe = checkBribe(bribe_id)

    c = Context({
        "bribe": bribe
    })
    return HttpResponse(t.render(c))



def track(request, bribe_id):

    bribe = checkBribe(bribe_id)

    return redirect('%s%s%s' % ('https://twitter.com/intent/tweet?text=', bribe.message, '&source=tweetbribe'))


def confirm(request, bribe_id):

    donate_url = '%s%s' % ('http://localhost:8080/bribe/donate/', bribe_id)

    bribe = checkBribe(bribe_id)

    return redirect('%s%s%s%s%s' % ('https://twitter.com/intent/tweet?text=@', bribe.briber.twitter_handle, ' - I just completed your @tweetbribe. Click here to donate ', donate_url, '&source=tweetbribe'))




def donate(request, bribe_id):

    t = loader.get_template('bribe/donate.html')

    c = Context({
    })
    return HttpResponse(t.render(c))

def checkBribe(bribe_id):
    bribe_list = Bribe.objects.filter(id__exact=bribe_id)
    

    if len(bribe_list) == 0:
        return False

    bribe = bribe_list[0]

    if not bribe:
        return False

    return bribe