
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import settings
from .views import DashboardView


urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("calendarapp.urls")),
    path("sport/", include("sport.urls", namespace="sport")),
    path('api/tg_users/', include('tg_users.urls')),
    path("select2/", include("django_select2.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
