from collections import OrderedDict

from rest_framework import serializers


class PrimaryKeyField(serializers.PrimaryKeyRelatedField):
    """
    Принимает первичный ключ в сериализатор, отдает данные из указанного сериализатора.
    """
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
        self.serializer = kwargs.pop('serializer', None)
        super(PrimaryKeyField, self).__init__(*args, **kwargs)

    def to_representation(self, value):
        pk = super(PrimaryKeyField, self).to_representation(value)
        try:
            item = self.model.objects.get(pk=pk)
            serializer = self.serializer(item)
            return serializer.data
        except self.model.DoesNotExist:
            return None

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        return OrderedDict([(item.id, str(item)) for item in queryset])
