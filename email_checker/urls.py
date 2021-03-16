from django.urls import path

from email_checker.views import download, make_checks

app_name = "email_checker"

urlpatterns = [
    path('get_csv/<int:id>', download, name='get_csv'),
    path('make_checks/<int:id>', make_checks, name='make_checks'),
]
