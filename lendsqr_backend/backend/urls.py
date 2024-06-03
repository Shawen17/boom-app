from django.contrib import admin
from django.urls import path, include
from lendsqr import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path(
        "api/users",
        views.users,
    ),
    path("api/update/user/<str:id>/<str:action>", views.update_status),
    path("api/advance-filter/", views.advance_filter),
    path(
        "api/get_staff_status/",
        views.get_staff_status,
    ),
    path(
        "api/add-staff-portfolio/",
        views.assign_user_to_portfolio,
    ),
    path(
        "api/loan/",
        views.new_loan,
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_DIR)
