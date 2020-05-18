from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices

__all__ = "Question",


class Question(models.Model):
    TypeChoices = Choices(
        ('text', _("Text")),
        ('one', _("One choice")),
        ('many', _("Many choices")),
    )

    poll = models.ForeignKey(
        'Poll',
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name=_("Poll"),
    )

    question = models.CharField(
        _("Question"),
        max_length=256,
    )
    question_type = models.CharField(
        _("Question type"),
        max_length=4,
        choices=TypeChoices,
    )

    class Meta:
        verbose_name = _("question")
        verbose_name_plural = _("questions")

    def __str__(self):
        return self.question
