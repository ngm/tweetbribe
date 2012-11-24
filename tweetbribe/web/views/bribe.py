from django.template import Context, loader, RequestContext
from django.http import HttpResponse
from web.models import Charity, Bribe
from django.shortcuts import redirect, render_to_response
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    t = loader.get_template('bribe/index.html')

    charities = Charity.objects.all()
    c = Context({
        "charities":charities
    })
    return HttpResponse(t.render(c))

@csrf_exempt
def create_bribe(request):
    errors = []
    if not request.POST.get('bribe_bribee_twitter_handle'):
        errors.append('Please enter a twitter handle for the person you are bribing!')
    if not request.POST.get('bribe_briber_twitter_handle'):
        errors.append('Please enter your twitter handle!')
    if not request.POST.get('bribe_message'):
        errors.append('Please enter some bribe text!')
    if not request.POST.get('bribe_charity_id'):
        errors.append('Please select a charity!')

    if len(errors) == 0:
        charity = Charity.objects.get(id=request.POST.get('bribe_charity_id'))
        bribe = Bribe()
        bribe.charity = charity
        bribe.briber_twitter_handle = request.POST.get('bribe_briber_twitter_handle')
        bribe.bribee_twitter_handle = request.POST.get('bribe_bribee_twitter_handle')
        bribe.message = request.POST.get('bribe_message')

        bribe.save()
        return render_to_response('bribe/success.html', {})

    charities = Charity.objects.all()
    c = Context({
        "charities":charities
    })
    
    return render_to_response('bribe/index.html', {'errors':errors, 'charities': charities})


def view(request, bribe_id):
    t = loader.get_template('bribe/view.html')

    bribe = checkBribe(bribe_id)
    donate_url = '%s%s' % ('http://localhost:8080/bribe/donate/', bribe_id)
    confirm_message = '%s%s%s%s' % ('@', bribe.briber_twitter_handle, ' - I just completed your @tweetbribe. Click here to donate ', donate_url)

    c = Context({
        "bribe": bribe,
        "confirm_message": confirm_message
    })
    return HttpResponse(t.render(c))


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
