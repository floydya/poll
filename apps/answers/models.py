from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = "PollAnswer", "QuestionAnswer",


class PollAnswer(models.Model):

    user_id = models.PositiveIntegerField(
        _("User ID"),
    )
    poll = models.ForeignKey(
        'polls.Poll',
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name=_("Poll"),
    )

    class Meta:
        verbose_name = _("poll answer")
        verbose_name_plural = _("poll answers")


class QuestionAnswer(models.Model):

    poll_answer = models.ForeignKey(
        PollAnswer,
        on_delete=models.CASCADE,
        related_name="question_answers",
        verbose_name=_("Poll answer")
    )

    question = models.ForeignKey(
        'polls.Question',
        on_delete=models.CASCADE,
        related_name="question_answers",
        verbose_name=_("Question"),
    )

    text_answer = models.TextField(
        _("Text answer"),
    )

    choice_answer = models.ManyToManyField(
        'polls.Choice',
    )
