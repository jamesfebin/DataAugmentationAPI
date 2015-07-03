
import requests
import json

class DataAPIS:

    def __init__(self):
        self.BRITEVERIFY_API_KEY = 'PLACE YOUR BRITEVERIFY API KEY HERE'

    def briteverify(self, email):
        try:
            r = requests.get('https://bpi.briteverify.com/emails.json?address='+email+'&apikey='+self.BRITEVERIFY_API_KEY)
            response = json.loads(r.text)

            if 'status' in response:
                return response['status']
            else:
                return 'API ERROR'
        except Exception as e:
            print e
            return 'API ERROR'
