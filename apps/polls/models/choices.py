from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = "Choice",


class Choice(models.Model):

    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        related_name="choices",
        verbose_name=_("Question"),
    )

    answer = models.CharField(
        _("Answer"),
        max_length=256,
    )

    class Meta:
        verbose_name = _("choice")
        verbose_name_plural = _("choices")

    def __str__(self):
        return self.answer
