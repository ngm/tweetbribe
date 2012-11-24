import urllib2

class giving_lab(object):

    def __init__(self):
        # todo: maybe move to local_settings.py
        # todo: maybe pass in as parameters
        self.api_key = "433b8c40-6ada-4b08-bc5c-cdd8a22d37b5"
        self.base_url = "https://www.thegivinglab.org/api"

    def get_charities(self):

        url = self.base_url + "/charities" + "?apikey=" + self.api_key

        try:
            data = urllib2.urlopen(url).read()
        except urllib2.HTTPError, e:
            print "HTTP error: %d" % e.code
        except urllib2.URLError, e:
            print "Network error: %s" % e.reason.args[1]

        return data

