"""This models.py contain Question, Choice class."""
import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """Question class contain method that manage about question in ku-polls."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end date', null=True)

    def __str__(self):
        """Str method for Question class."""
        return self.question_text

    def was_published_recently(self):
        """Methods that check if question was published in previous time."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Methods that check if question is published."""
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """Methods to check that user can vote question."""
        now = timezone.now()
        # if now >= self.pub_date or self.end_date:
        #     return True
        # return self.end_date >= now >= self.pub_date
        return self.pub_date <= now <= self.end_date


class Choice(models.Model):
    """Choice class contain information about choices in question."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    # votes = models.IntegerField(default=0)

    def __str__(self):
        """Str method for Choice class."""
        return self.choice_text

    @property
    def votes(self):
        count = Vote.objects.filter(choice=self).count()
        return count


class Vote(models.Model):
    """Represents a vote made by a user"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"Voted by {self.user.username} for {self.choice.choice_text}"
