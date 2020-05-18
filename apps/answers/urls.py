from rest_framework.routers import SimpleRouter

from apps.answers.viewsets import PollAnswerViewSet

router = SimpleRouter()

router.register("answers", PollAnswerViewSet, basename="answers")

urlpatterns = router.urls
