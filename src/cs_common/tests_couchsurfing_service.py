from django.test import TestCase
import json
from PACouchsurfing.settings import get_secret
from cs_common.couchsurfing_service import CouchsurfingService


class CouchsurfingTestCase(TestCase):
    def setUp(self):
        email = get_secret('TEST_USER_EMAIL')
        password = get_secret('TEST_USER_PASSWORD')
        self.cs = CouchsurfingService(email, password)

    def test_get_friendlist(self):
        generated_friendlist = self.cs.get_friendlist()
        print(json.dumps(generated_friendlist, indent=4))
