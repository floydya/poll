import json
from datetime import timedelta

from django.test import TestCase
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.answers.models import PollAnswer
from apps.answers.serializers import QuestionAnswerSerializer, PollAnswerSerializer
from apps.polls.models import Poll, Question, Choice


class SerializerTestCase(TestCase):

    @classmethod
    def setUp(cls) -> None:

        cls.poll = Poll.objects.create(
            title="Poll title",
            start_date=now(),
            end_date=now() + timedelta(days=7),
            description="Poll description"
        )
        cls.text_question = Question.objects.create(poll=cls.poll, question="Your name?",
                                                    question_type=Question.TypeChoices.text)
        cls.one_question = Question.objects.create(poll=cls.poll, question="Color?",
                                                   question_type=Question.TypeChoices.one)
        cls.many_question = Question.objects.create(poll=cls.poll, question="Choose 1 and 3 options",
                                                    question_type=Question.TypeChoices.many)
        Choice.objects.bulk_create([
            Choice(question=cls.one_question, answer="Red"),
            Choice(question=cls.one_question, answer="Green"),
            Choice(question=cls.one_question, answer="Blue"),
            Choice(question=cls.many_question, answer="First"),
            Choice(question=cls.many_question, answer="Second"),
            Choice(question=cls.many_question, answer="Third"),
        ])

    def error_test(self, input_data, error_data):
        serializer = QuestionAnswerSerializer(data=input_data)
        try:
            serializer.is_valid(raise_exception=True)
            self.fail()
        except ValidationError as err:
            self.assertJSONEqual(json.dumps(err.detail), error_data)

    def test_question_answer_serializer_text(self):
        self.error_test(
            input_data={"question": self.text_question.id, "choice_answer": [Choice.objects.first().pk]},
            error_data={'text_answer': [_("This field is required!")]}
        )

    def test_question_answer_serializer_choice(self):
        self.error_test(
            input_data={"question": self.one_question.id, "text_answer": "test"},
            error_data={'choice_answer': [_("This field is required!")]}
        )

    def test_question_answer_serializer_one_choice(self):
        self.error_test(
            input_data={"question": self.one_question.id,
                        "choice_answer": self.one_question.choices.values_list('id', flat=True)},
            error_data={'choice_answer': [_("Only one choice can be selected!")]}
        )

    def test_question_answer_serializer_many_choice(self):
        self.error_test(
            input_data={"question": self.many_question.id, "choice_answer": []},
            error_data={'choice_answer': [_("This field is required!")]}
        )

    def test_question_answer_serializer_another_choices(self):
        choices = self.one_question.choices.all()
        self.error_test(
            input_data={"question": self.many_question.id, "choice_answer": choices.values_list('id', flat=True)},
            error_data={'choice_answer': ["Answer 'Red' <1> not valid for this question!"]}
        )

    def test_question_answer_serializer_validated_success(self):
        choice = self.one_question.choices.first().pk
        input_data = {"question": self.one_question.id, "choice_answer": [choice]}
        serializer = QuestionAnswerSerializer(data=input_data)
        serializer.is_valid(raise_exception=True)

    def test_poll_answer_serializer_not_valid(self):
        serializer = PollAnswerSerializer(
            data={
                "user_id": 1,
                "poll": self.poll.pk,
                "question_answers": [
                    {"question": self.text_question.pk, "text_answer": "test"},
                ]
            }
        )
        try:
            serializer.is_valid(raise_exception=True)
            self.fail()
        except ValidationError as err:
            self.assertJSONEqual(
                json.dumps(err.detail),
                {'non_field_errors': [
                    {'question_answers': "Answer on 'Color?' <2> question is required!"},
                    {'question_answers': "Answer on 'Choose 1 and 3 options' <3> question is required!"},
                ]}
            )

    def test_poll_answer_serializer_created_successfully(self):
        serializer = PollAnswerSerializer(
            data={
                "user_id": 1,
                "poll": self.poll.pk,
                "question_answers": [
                    {"question": self.text_question.pk, "text_answer": "test"},
                    {"question": self.one_question.pk, "choice_answer": [
                        self.one_question.choices.first().pk
                    ]},
                    {"question": self.many_question.pk, "choice_answer":
                        self.many_question.choices.values_list('id', flat=True)
                     },
                ]
            }
        )
        serializer.is_valid(raise_exception=True)
        instance: PollAnswer = serializer.save()

        self.assertEqual(instance.user_id, 1)
        self.assertEqual(instance.poll.pk, self.poll.pk)
        self.assertEqual(
            list(instance.question_answers.get(question=self.many_question).choice_answer.values_list('id', flat=True)),
            [4, 5, 6]
        )
