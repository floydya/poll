from django.contrib import admin

from apps.polls.models import Poll, Question, Choice


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    fields = ('title', 'start_date', 'end_date', 'description')

    def get_readonly_fields(self, request, obj=None):
        if getattr(obj, "pk", None):
            return ["start_date"]
        return super(PollAdmin, self).get_readonly_fields(request, obj)


class ChoiceInline(admin.TabularInline):
    model = Choice
    fk_name = "question"
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = (ChoiceInline,)

    def get_inline_instances(self, request, obj=None):
        CHOICES_TYPES = (Question.TypeChoices.one, Question.TypeChoices.many)
        if getattr(obj, "question_type", None) not in CHOICES_TYPES:
            return []
        return super(QuestionAdmin, self).get_inline_instances(request, obj)

