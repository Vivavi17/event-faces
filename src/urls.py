from django.contrib import admin
from django.urls import include, path

from src.events.urls import router

urlpatterns = [
    path("api/", include(router.urls)),
    path("admin/", admin.site.urls),
]
