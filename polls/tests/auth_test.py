"""This auth_test.py contain test case for testing Authentication in ku-polls."""
import datetime


import django.test
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from polls.models import Question


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the.

    given number of `days` offset to now (negative for questions published.
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time,
                                   end_date=time + datetime.timedelta(days=6))


class UserAuthTest(django.test.TestCase):

    def setUp(self):
        super().setUp()
        self.username = "testuser"
        self.password = "Fat-Chance!"
        self.user1 = User.objects.create_user(
            username=self.username,
            password=self.password,
            email="testuser@nowhere.com")
        self.user1.first_name = "Tester"
        self.user1.save()
        # need a poll question to test voting
        self.question = create_question(question_text="First Poll Question", days=1)

    def test_login_view(self):
        """Test that a user can login via the login view."""
        login_url = reverse("login")
        # Can get the login page
        response = self.client.get(login_url)
        self.assertEqual(200, response.status_code)
        # Can login using POST
        # usage: client.post(url, {'key1":"value", "key2":"value"})
        form_data = {"username": self.username, "password": self.password}
        response = self.client.post(login_url, form_data)
        self.assertEqual(302, response.status_code)
        # should redirect us to the polls index page ("polls:index")
        self.assertRedirects(response, reverse("polls:index"))

    def test_logout_view(self):
        """Test that a user can logout via the logout view."""
        logout_url = reverse("logout")
        response = self.client.get(logout_url)
        self.assertEqual(200, response.status_code)

    def test_not_login_vote(self):
        """Check that it will redirect to login page if vote when not login yet"""
        response = self.client.get(reverse('polls:vote', args=(self.question.id,)))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/polls/1/vote/')