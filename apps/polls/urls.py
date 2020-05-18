from django.urls import path

from apps.polls.viewsets import ActivePollListView

urlpatterns = [
    path("polls/", ActivePollListView.as_view(), name="active-poll-list"),
]