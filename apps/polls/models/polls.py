from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = "Poll",

from apps.polls.managers import PollQuerySet


class Poll(models.Model):

    title = models.CharField(
        _("Title"),
        max_length=256
    )
    start_date = models.DateTimeField(
        _("Start date"),
    )
    end_date = models.DateTimeField(
        _("End date"),
    )
    description = models.TextField(
        _("Description")
    )

    objects = models.Manager.from_queryset(PollQuerySet)()

    class Meta:
        verbose_name = _("poll")
        verbose_name_plural = _("polls")

    def __str__(self):
        return self.title
