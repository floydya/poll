from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Polls API",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + [
    path('admin/', admin.site.urls),
    path('', include("apps.polls.urls")),
    path('', include("apps.answers.urls")),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0)),
]
