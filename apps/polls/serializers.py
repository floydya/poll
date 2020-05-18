from rest_framework import serializers

from apps.polls.models import Poll, Question, Choice

__all__ = (
    "ChoiceSerializer",
    "QuestionSerializer", "ExtendedQuestionSerializer",
    "PollSerializer", "ExtendedPollSerializer"
)


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = (
            'id', 'answer'
        )


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = (
            'id', 'question', 'question_type',
        )


class ExtendedQuestionSerializer(QuestionSerializer):

    choices = ChoiceSerializer(many=True)

    class Meta(QuestionSerializer.Meta):
        fields = (*QuestionSerializer.Meta.fields, 'choices',)


class PollSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poll
        fields = (
            'id', 'title', 'start_date', 'end_date', 'description',
        )


class ExtendedPollSerializer(PollSerializer):
    questions = ExtendedQuestionSerializer(many=True)

    class Meta(PollSerializer.Meta):
        fields = (*PollSerializer.Meta.fields, 'questions',)
