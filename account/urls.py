from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from account.views import FirstRegistrationView, LastRegistrationView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('first-register/', FirstRegistrationView.as_view(), name='first-register'),
    path('last-register/', LastRegistrationView.as_view(), name='last-register'),

]
