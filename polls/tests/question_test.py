"""This question_test.py contain test case for testing Question's method of ku-polls."""
import datetime

from django.test import TestCase
from django.utils import timezone

from polls.models import Question


class QuestionTests(TestCase):
    """QuestionTests contain test for methods in models.py."""

    def test_is_published(self):
        """
        is_published() returns True for questions whose pub_date.

        is within the present time.
        """
        time = timezone.now() - datetime.timedelta(days=1)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.is_published(), True)

    def test_can_vote(self):
        """
        can_vote() returns True for questions whose pub_date.

        is within the present day and the present day is.
        within end_date.
        """
        pub_time = timezone.now()
        end_time = timezone.now() + timezone.timedelta(hours=10)
        question_1 = Question(pub_date=pub_time, end_date=end_time)
        self.assertIs(question_1.can_vote(), True)
