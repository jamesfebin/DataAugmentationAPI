
import requests
import json
from solve360 import Solve360
from relateiq.client import RelateIQ
from relateiq.contacts import Contact

class DataAPIS:

    def __init__(self):
        self.BRITEVERIFY_API_KEY = '4eba6214-6178-4624-ab83-4f84037413da'
        self.solve360_EMAIL='jamesfebin@gmail.com'
        self.solve360_API_TOKEN='BeO6l634r3Rfq8j9tfw9B3Q3e1c2Har0Neo7ceG2'
        self.relateIQ_API_KEY='55a895ece4b0b45e109ec7ee'
        self.relateIQ_API_SECRET='0Avcujw70WHGpEIhXFeigFU24fW'
        self.airtable_API_KEY='keyopGxEcKCs2ZOND'
        self.fullcontact_API_KEY='15edc76d93d8d49e'

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

    def solve360(self,email):
        try:
            crm = Solve360(self.solve360_EMAIL, self.solve360_API_TOKEN)
            list=crm.list_contacts(filtermode='byemail',searchvalue=email)
            if 'count' in list:
                if list['count'] > 0 :
                    return 'exists'

            return 'Doesn\'t exist'
        except Exception as e:
            print e
            return 'API ERROR'


    def relateiq(self,email):
        try:
            RelateIQ("55a895ece4b0b45e109ec7ee","0Avcujw70WHGpEIhXFeigFU24fW")
            contact=Contact(email)
            data = contact._properties 
            company = ''
            if 'company' in data:
                company = contact._properties['email'][0]['value']
            
        except Exception, e:
            print e
            return 'API ERROR'

    def airtable(self,company):
        try:
            pass
        except Exception as e:
            print e
            return 'API ERROR'
    def fullcontact(self,email):
        try:
            url='https://api.fullcontact.com/v2/person.json'
            kwargs = {}
            kwargs['apiKey'] = self.fullcontact_API_KEY
            kwargs['email'] = email
            r = requests.get(url, params=kwargs)
            r= json.loads(r.text)
            return r
        except Exception as e:
            print e
            return 'API ERROR'


