from django.db.models import QuerySet
from django.utils.timezone import now

__all__ = "PollQuerySet",


class PollQuerySet(QuerySet):

    def active(self):
        return self.filter(end_date__gt=now())
