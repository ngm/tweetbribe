from django.template import Context, loader, RequestContext
from django.http import HttpResponse
from web.models import Charity, Bribe
from django.shortcuts import redirect, render_to_response
from django.views.decorators.csrf import csrf_exempt

def setup(request):

    Charity.objects.all().delete()

    charities = []
    charities.append(Charity(name='Child And Sound Limited', description='', givinglab_id='83446196-b8dc-4e1e-a02c-002cc96843f3', logo_url=''))
    charities.append(Charity(name='Academy Fm Folkestone', description='', givinglab_id='e7f67c66-9ecb-4a2c-aef4-0051aa36eee5', logo_url=''))
    charities.append(Charity(name='Kids At School In Nepal', description='', givinglab_id='479a5f6c-3885-48be-ad94-007998942d82', logo_url=''))
    charities.append(Charity(name='Nepal- England Education Support', description='', givinglab_id='241b75e8-dcb2-4db1-be8d-00871ae90312', logo_url=''))
    charities.append(Charity(name='Gladstone Theatre Trust', description='', givinglab_id='4d7b7bd4-e944-4d6d-b777-00c12c070abf', logo_url=''))
    charities.append(Charity(name='Child And Sound Limited', description='', givinglab_id='83446196-b8dc-4e1e-a02c-002cc96843f3', logo_url=''))
    charities.append(Charity(name='Academy Fm Folkestone', description='', givinglab_id='e7f67c66-9ecb-4a2c-aef4-0051aa36eee5', logo_url=''))
    charities.append(Charity(name='Kids At School In Nepal', description='', givinglab_id='479a5f6c-3885-48be-ad94-007998942d82', logo_url=''))
    charities.append(Charity(name='Nepal- England Education Support', description='', givinglab_id='241b75e8-dcb2-4db1-be8d-00871ae90312', logo_url=''))
    charities.append(Charity(name='Gladstone Theatre Trust', description='', givinglab_id='4d7b7bd4-e944-4d6d-b777-00c12c070abf', logo_url=''))
    charities.append(Charity(name='Child And Sound Limited', description='', givinglab_id='83446196-b8dc-4e1e-a02c-002cc96843f3', logo_url=''))
    charities.append(Charity(name='Academy Fm Folkestone', description='', givinglab_id='e7f67c66-9ecb-4a2c-aef4-0051aa36eee5', logo_url=''))
    charities.append(Charity(name='Kids At School In Nepal', description='', givinglab_id='479a5f6c-3885-48be-ad94-007998942d82', logo_url=''))
    charities.append(Charity(name='Nepal- England Education Support', description='', givinglab_id='241b75e8-dcb2-4db1-be8d-00871ae90312', logo_url=''))
    charities.append(Charity(name='Gladstone Theatre Trust', description='', givinglab_id='4d7b7bd4-e944-4d6d-b777-00c12c070abf', logo_url=''))

    for charity in charities:
        charity.save()

@csrf_exempt
def index(request, *args):
    print args
    if len(args) == 2:
        briber, bribee = args
    else:
        bribee = ''
        briber = ''
    t = loader.get_template('bribe/index.html')

    charities = addDefaultImage(Charity.objects.all())


    print bribee, briber

    c = Context({
        "charities":charities,
        "bribee":bribee,
        "briber":briber
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



    briber = request.POST.get('bribe_briber_twitter_handle')
    bribee = request.POST.get('bribe_bribee_twitter_handle')

    if len(errors) == 0:
        charity = Charity.objects.get(id=request.POST.get('bribe_charity_id'))
        bribe = Bribe()
        bribe.charity = charity
        bribe.briber_twitter_handle = request.POST.get('bribe_briber_twitter_handle')
        bribe.bribee_twitter_handle = request.POST.get('bribe_bribee_twitter_handle')
        bribe.message = request.POST.get('bribe_message')

        bribe.save()
        bribe_url = '%s%s' % ('http://localhost:8080/bribe/view/', bribe.id)
        return render_to_response('bribe/success.html', {'bribe':bribe, 'bribe_url':bribe_url})

    charities = addDefaultImage(Charity.objects.all())
    c = Context({
        "charities":charities,
        "bribee":bribee,
        "briber":briber
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
    bribe = checkBribe(bribe_id)

    c = Context({
        "bribe": bribe,
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

def addDefaultImage(charities):
    for charity in charities:
        if not charity.logo_url or charity.logo_url.strip() == "":
            charity.logo_url = '/static/images/charity_placeholder.png'

    return charities
