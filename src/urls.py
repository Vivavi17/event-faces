from django.contrib import admin
from django.urls import include, path

from src.events.urls import router
from src.userauth.urls import urlpatterns as auth_url

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/auth/", include(auth_url)),
    path("admin/", admin.site.urls),
]
