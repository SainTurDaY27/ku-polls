"""This views.py contain IndexView, DetailView, ResultView class."""
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Choice, Question, Vote


class IndexView(generic.ListView):
    """IndexView class contain get_queryset method."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions.

        (not including those set to be published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """DetailView class contain get_queryset, get method."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any question that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """
        Methods that manage about redirect and return error message.

        If question can vote, redirect to
        """
        self.object = self.get_object()
        if not self.object.can_vote():
            messages.error(request, 'This poll is not allowed to vote.')
            return redirect('polls:index')
        else:
            return render(request, self.template_name, self.get_context_data())


class ResultView(generic.DetailView):
    """ResultView class contain model and template name."""

    model = Question
    template_name = 'polls/results.html'


def get_vote_for_user(user, question):
    """
    Find and return an existing vote for a user on a poll question.
    Returns:
        The user's vote or None if there are no votes for this question.
    """
    try:
        votes = Vote.objects.filter(user=user).filter(choice__question=question)
        if votes.count() == 0:
            return None
        return votes[0]
    except Vote.DoesNotExist:
        return None


@login_required(login_url='/accounts/login/')
def vote(request, question_id):
    """
    Methods that manage about redirect when user have vote.

    and return error message when vote is not allowed.
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        user = request.user
        user_vote = get_vote_for_user(user, question)
        if user_vote is None:
            user_vote = Vote.objects.create(user=user, choice=selected_choice)
        else:
            user_vote.choice = selected_choice
        user_vote.save()
        return HttpResponseRedirect(reverse('polls:results',
                                            args=(question.id,)))

