from rest_framework.generics import ListAPIView

from apps.polls.models import Poll
from apps.polls.serializers import ExtendedPollSerializer


class ActivePollListView(ListAPIView):
    serializer_class = ExtendedPollSerializer
    queryset = Poll.objects.all().active()
