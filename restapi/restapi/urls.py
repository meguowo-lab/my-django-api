"""URL configuration for restapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/

Examples
--------
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""

from api.views import router, verify_email_complete_view, verify_email_view
from django.contrib import admin
from django.contrib.auth import views
from django.urls import include, path

reset_password_patterns = [
    path("", views.PasswordResetView.as_view()),
    path(
        "confirm/<str:uidb64>/<str:token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "complete/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("done/", views.PasswordResetDoneView.as_view(), name="password_reset_done"),
]

change_password_patterns = [
    path("", views.PasswordChangeView.as_view()),
    path("done/", views.PasswordChangeDoneView.as_view(), name="password_change_done"),
]

auth_patterns = [
    path("", include("rest_framework.urls", namespace="rest_framework")),
    path("reset_password/", include(reset_password_patterns)),
    path("change_password/", include(change_password_patterns)),
]

email_verify_patterns = [
    path(
        "<int:pk>/<str:token>/",
        verify_email_complete_view,
        name="email_verify",
    ),
    path("", verify_email_view, name="verify_email"),
]

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("admin/", admin.site.urls),
    path("email-verify/", include(email_verify_patterns)),
    path("api-auth/", include(auth_patterns)),
]
