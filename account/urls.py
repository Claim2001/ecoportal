from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from account.views import RegistrationView, CodeConfirmView, SendSMSView

urlpatterns = [
    path('login/', SendSMSView.as_view(), name='login'),
    path('confirm/', CodeConfirmView.as_view(), name='code_confirm'),
    path('register/', RegistrationView.as_view(), name='registration'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
