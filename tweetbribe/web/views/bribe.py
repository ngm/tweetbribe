from django.template import Context, loader, RequestContext
from django.http import HttpResponse
from web.models import Charity, Bribe
from django.shortcuts import redirect, render_to_response
from django.views.decorators.csrf import csrf_exempt
import urllib2
import json 

#URL = 'localhost:8080'
URL = 'http://www.tweetbribe.com'

def setup(request):

    Charity.objects.all().delete()

    charities = []
    charities.append(Charity(name='British Heart Foundation', description='', givinglab_id='3eb39186-e8a6-4495-ba38-588409080124', logo_url='bhf_logo.jpg'))
    charities.append(Charity(name='Stroke Association', description='', givinglab_id='833422b4-f47d-4511-b5fb-eacb33c59c16', logo_url='/static/logos/strokeassoc.jpg'))
    charities.append(Charity(name='Academy Fm Folkestone', description='', givinglab_id='479a5f6c-3885-48be-ad94-007998942d82', logo_url='/static/logos/academy_fm_folkestone.jpg'))
    charities.append(Charity(name='Multiple Sclerosis Society', description='', givinglab_id='149a4a4a-7c0d-4ac1-93f4-21038bdf8398', logo_url='/static/logos/mssoc.jpeg'))
   
    charities.append(Charity(name='Cancer Buddies Network', description='', givinglab_id='511a32f-b18e-4dfc-9134-aac25c2f0a9b', logo_url='/static/logos/cancerbuddiesnetwork.jpg'))
    charities.append(Charity(name='Cancer Recovery Foundation Uk', description='', givinglab_id='a7f94cd9-b0d7-444a-bfab-c24e5ce4b7ad', logo_url='/static/logos/cancer_recovery_trust.jpg'))
    charities.append(Charity(name='Action For Children', description='', givinglab_id='3e4e9efa-951a-4fa0-8390-47ec999dd8ca', logo_url='/static/logos/action_for_children.jpg'))
    charities.append(Charity(name='Tree of Hope', description='', givinglab_id='18fb1d04-f657-4792-99df-2fc194565be3', logo_url='/static/logos/tree_of_hope.jpg'))
    charities.append(Charity(name='Variety Club', description='', givinglab_id='ff6ccd27-c61a-48e5-9b24-4fbb9ca0ac94', logo_url='/static/logos/variety_club.jpg'))
    charities.append(Charity(name='Global Children Development', description='', givinglab_id='2d2e32e6-a1f7-49ce-9287-125f16a7638a', logo_url='/static/logos/global_childrens_development.jpg'))
    
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
        bribe_url = '%s%s' % (URL + '/bribe/view/', bribe.id)
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
    donate_url = '%s%s' % (URL + '/bribe/donate/', bribe_id)
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


def bitlyurl(long_url):


    try:
        data = urllib2.urlopen('https://api-ssl.bitly.com/v3/shorten?access_token=bfd00e2e1bd539db7f87ee2bd3f1febdc186fbc5&longUrl=' + long_url).read()

        data = json.loads(data)
        print data, 'sdf',

    except urllib2.HTTPError, e:
        print "HTTP error: %d" % e.code
    except urllib2.URLError, e:
        print "Network error: %s" % e.reason.args[1]




