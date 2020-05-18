from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from apps.answers.models import PollAnswer, QuestionAnswer
from apps.polls.models import Poll, Question, Choice
from apps.polls.serializers import PollSerializer, QuestionSerializer, ChoiceSerializer
from shared.fields import PrimaryKeyField


class QuestionAnswerSerializer(serializers.ModelSerializer):
    question = PrimaryKeyField(
        model=Question,
        queryset=Question.objects.all(),
        serializer=QuestionSerializer
    )

    choice_answer = PrimaryKeyField(
        model=Choice,
        serializer=ChoiceSerializer,
        queryset=Choice.objects.all(),
        many=True,
        required=False
    )
    text_answer = serializers.CharField(required=False)

    def validate(self, attrs):

        question: Question = attrs.get('question')

        if question.question_type == Question.TypeChoices.text:
            if attrs.get('choice_answer'):
                attrs['choice_answer'] = []

            if not attrs.get('text_answer'):
                raise serializers.ValidationError({"text_answer": _("This field is required!")})
        else:
            if attrs.get('text_answer'):
                attrs['text_answer'] = ""

            if question.question_type == Question.TypeChoices.one:
                if not attrs.get('choice_answer'):
                    raise serializers.ValidationError({"choice_answer": _("This field is required!")})
                elif len(attrs.get('choice_answer')) > 1:
                    raise serializers.ValidationError({"choice_answer": _("Only one choice can be selected!")})
            else:
                if not attrs.get('choice_answer'):
                    raise serializers.ValidationError({"choice_answer": _("This field is required!")})

            for answer in attrs.get('choice_answer'):
                if answer.question != question:
                    raise serializers.ValidationError(
                        {"choice_answer": "Answer '{}' <{}> not valid for this question!".format(answer, answer.pk)}
                    )

        return attrs

    class Meta:
        model = QuestionAnswer
        fields = ("id", "question", "text_answer", "choice_answer")


class PollAnswerSerializer(serializers.ModelSerializer):
    poll = PrimaryKeyField(
        model=Poll,
        queryset=Poll.objects.all(),
        serializer=PollSerializer
    )

    question_answers = QuestionAnswerSerializer(many=True)

    def validate(self, attrs):
        poll: Poll = attrs.get('poll')
        question_answers: list = attrs.get('question_answers')
        question_keys = (q.get('question').pk for q in question_answers)
        if answers_remained := poll.questions.exclude(pk__in=question_keys):
            raise serializers.ValidationError(list(
                { "question_answers": f"Answer on '{question}' <{question.id}> question is required!"}
                for question in answers_remained
            ))
        return attrs

    class Meta:
        model = PollAnswer
        fields = ('id', 'user_id', 'poll', 'question_answers')

    @transaction.atomic
    def create(self, validated_data):
        question_answers = validated_data.pop('question_answers')
        instance = PollAnswer.objects.create(**validated_data)
        for answer in question_answers:
            choices = answer.pop("choice_answer", None)
            q_answer = QuestionAnswer.objects.create(poll_answer=instance, **answer)
            if choices:
                q_answer.choice_answer.set(choices)
        return instance
