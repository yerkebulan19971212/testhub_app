from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from django.conf.urls.static import static

api_v1_urlpatterns = [
    path('user/', include('accounts.urls')),
    path('quizes/', include('quizzes.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-panel/', include('admin_panel.urls')),
    path('api/v1/', include(api_v1_urlpatterns)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
