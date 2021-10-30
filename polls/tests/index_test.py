"""This index_test.py contain test case for testing Index model of ku-polls."""
import datetime

from django.test import TestCase
from django.utils import timezone
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


class QuestionIndexViewTests(TestCase):
    """QuestionIndexTests contain test for methods that manage index page."""

    def test_no_question(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past.

        displays the question's text.
        """
        create_question(
            question_text='Past Question.', days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past Question.>']
        )

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future.

        returns None when call a question.
        """
        future_question = create_question(
            question_text='Future question.', days=5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        self.assertFalse(future_question.can_vote())

    def test_future_question_and_past_question(self):
        """
        Even if both past and future question exist, only past questions.

        are displayed.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

    def test_past_question_after_end_date(self):
        """
        Test about past question that pass the end date of itself.

        It will not allowed to vote.
        """
        past_question = create_question(
            question_text='After end date Question.', days=-7)
        response = self.client.get(reverse('polls:index'))
        self.assertFalse(past_question.can_vote())
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: After end date Question.>']
        )