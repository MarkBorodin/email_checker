from django.urls import path

from email_checker.views import download

app_name = "email_checker"

urlpatterns = [
    path('get_csv/<int:id>', download, name='get_csv'),
]
