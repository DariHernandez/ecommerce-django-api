from django.test import TestCase
from django.urls import reverse

# Tets variables
api_key = "ddffbffd1937c881541c1e749d3235d5"
user = "sample"
redirect = "http://www.darideveloper.com/"

class TestApi (TestCase):
    
    
    def test_post (self):

        data = {
            "api_key": api_key,
            "user": user,
            "redirect": redirect
        }        
        response = self.client.post(reverse("contactforms:index"), data)
        self.assertIn("text/html", response.headers["Content-Type"])

    def test_post_no_arguments (self):
    
        response = self.client.post(reverse("contactforms:index"))
        self.assertEqual(400, response.status_code)

    def test_post_wrong_arguments (self):

        data = {
            "api_key": "",
            "user": "",
            "redirect": ""
        }    
        
        response = self.client.post(reverse("contactforms:index"), data)
        self.assertEqual(400, response.status_code)

