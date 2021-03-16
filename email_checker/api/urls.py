from django.urls import path

from email_checker.api.views import EmailCheckView

app_name = 'email_checker_api'

urlpatterns = [
    path('email_check/', EmailCheckView.as_view(), name='email_check'),
]
