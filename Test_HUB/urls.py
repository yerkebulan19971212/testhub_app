from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings

from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from quizzes.urls import (
    favorite_urlpatterns,
    tag_urlpatterns,
    ent_urlpatterns,
    info_urlpatterns
)


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

api_v1_urlpatterns = [
    path('user/', include('accounts.urls')),
    path('quizes/', include('quizzes.urls')),
    path('favorite/', include(favorite_urlpatterns)),
    path('tag/', include(tag_urlpatterns)),
    path('full-test/', include(ent_urlpatterns)),
    path('info/', include(info_urlpatterns)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-panel/', include('admin_panel.urls')),
    path('api/v1/', include(api_v1_urlpatterns)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
