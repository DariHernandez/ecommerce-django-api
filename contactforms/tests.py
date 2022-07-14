from . import config
from . import models
from .email_manager.reader import Email_manager

from django.test import TestCase
from django.urls import reverse

class TestApi (TestCase):

    def __create_data (self):
        """Create register in test database an user, from email and blacklist"""

        # Get credentials
        credentials = config.Config()
        self.api_key = credentials.get('api_key')
        self.user = credentials.get('user')
        self.to_email = credentials.get('to_email')
        self.redirect = credentials.get('redirect')
        self.from_email = credentials.get('from_email')
        self.from_password = credentials.get('from_password')
        self.blackList_email = credentials.get('blackList_email')

        user = models.User(name=self.user,
                            api_key=self.api_key,
                            to_email=self.to_email)
        user.save()

        from_email = models.FromEmail (email=self.from_email,
                                        password=self.from_password)
        from_email.save ()

        blacklist = models.BlackList (to_email=self.blackList_email)
        blacklist.save()

    def __validate_email (self, subject="New contact message!", email_send=True):
        """Login to gmail and validate the last email

        Args:
            subject (str, optional): The value of the subject in the ast email. Defaults to "New contact message!".
            email_send (bool, optional): Validate if the email its send (True) or if the email have been omitted (False). Defaults to True.
        """


        # Login to gmail and read last email
        emailer = Email_manager (self.from_email, self.from_password)
        emailer.set_folder ("[Gmail]/Sent Mail")
        uids = emailer.get_uids (last_emails_num=1)
        self.assertEqual (len(uids), 1)
        emails = emailer.get_emals (uids)
        self.assertEqual (len(emails), 1)

        # Get email parts
        to_mail = emails[0]["to_email"][0]
        email_subject = emails[0]["subject"]

        # Validate email parts
        if email_send:
            self.assertEqual (to_mail, self.to_email)
            if subject:
                self.assertEqual (email_subject, subject)
        else:
            subject_email_match = False
            if to_mail == self.to_email and email_subject == subject :
                subject_email_match = True

            self.assertFalse (subject_email_match)

    def test_get_no_arguments(self):
        
        # Api Call
        response = self.client.get(reverse("contactforms:index"))

        # Test response
        self.assertEqual(405, response.status_code)


    def test_get_wrong_arguments(self):

        # API call
        data = {
            "api_key": "",
            "user": "",
            "redirect": ""
        }
        response = self.client.get(reverse("contactforms:index"), data)

        # Test response
        self.assertEqual(405, response.status_code)


    def test_post_no_arguments(self):
        
        # Api Call
        response = self.client.post(reverse("contactforms:index"))

        # Test response
        self.assertEqual(400, response.status_code)
        self.assertEqual(b'Invalid form structure', response.content)


    def test_post_wrong_arguments(self):

        # API call
        data = {
            "api_key": "",
            "user": "",
            "redirect": ""
        }
        response = self.client.post(reverse("contactforms:index"), data)

        # Test response
        self.assertEqual(400, response.status_code)
        self.assertEqual(b'invalid api key or user name', response.content)


    def test_post_no_subject (self):

        self.__create_data ()

        # Api call
        data = {
            "api_key": self.api_key,
            "user": self.user,
            "redirect": self.redirect,
        }
        response = self.client.post(reverse("contactforms:index"), data)

        # Validate response
        self.assertEqual(response.status_code, 302)

        # Validate history
        history_rows = models.History.objects.all()
        users = models.User.objects.all()
        self.assertEqual(len(history_rows), 1)
        self.assertEqual(len(users), 1)
        self.assertEqual(history_rows[0].user, users[0])

        # Check email in send mailbox
        self.__validate_email ()

    def test_post_subject (self):
    
        self.__create_data ()

        # Api call
        subject = "my test email"
        data = {
            "api_key": self.api_key,
            "user": self.user,
            "redirect": self.redirect,
            "subject": subject
        }
        response = self.client.post(reverse("contactforms:index"), data)

        # Validate response
        self.assertEqual(response.status_code, 302)

        # Validate history
        history_rows = models.History.objects.all()
        users = models.User.objects.all()
        self.assertEqual(len(history_rows), 1)
        self.assertEqual(len(users), 1)
        self.assertEqual(history_rows[0].user, users[0])

        # Check email in send mailbox
        self.__validate_email (subject)

    def test_post_blackList_email (self):
        
        self.__create_data ()

        # Api call
        subject = "my spam test email"
        data = {
            "api_key": self.api_key,
            "user": self.user,
            "redirect": self.redirect,
            "subject": subject,
            "email": self.blackList_email
        }
        response = self.client.post(reverse("contactforms:index"), data)

        # Validate response
        self.assertEqual(response.status_code, 302)

        # Validate history
        history_rows = models.History.objects.all()
        users = models.User.objects.all()
        self.assertEqual(len(history_rows), 1)
        self.assertEqual(len(users), 1)
        self.assertEqual(history_rows[0].user, users[0])
        self.assertIn ("Spam try from", history_rows[0].subject)

        # Check email in send mailbox
        self.__validate_email (subject, email_send=False)