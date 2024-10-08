from django.contrib import admin
from django.urls import path, include
from lendsqr import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", include("django_prometheus.urls")),
    path("metrics", views.metrics_view, name="metrics"),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("api/users", views.users, name="users"),
    path("api/update/user/<str:id>/<str:action>", views.update_status, name="status"),
    path("api/advance-filter", views.advance_filter, name="advance_filter"),
    path("api/get_staff_status/", views.get_staff_status, name="staff_staus"),
    path("api/add-staff-portfolio/", views.assign_user_to_portfolio, name="porfolio"),
    path("api/loan/", views.new_loan, name="loan"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_DIR)
