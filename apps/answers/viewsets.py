from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from apps.answers.models import PollAnswer
from apps.answers.serializers import PollAnswerSerializer


class PollAnswerViewSet(ModelViewSet):
    queryset = PollAnswer.objects.prefetch_related('question_answers').all()
    serializer_class = PollAnswerSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = "user_id",
