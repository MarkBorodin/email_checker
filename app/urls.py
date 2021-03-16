from django.contrib import admin
from django.urls import path, include

API_PREFIX = 'api/v1'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('email_checker.urls')),


    # API
    path(f'{API_PREFIX}', include('email_checker.api.urls')),
    # path(f'{API_PREFIX}/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path(f'{API_PREFIX}/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
