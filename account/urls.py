from django.urls import path
from knox import views as knox_views

from account.views import RegistrationView, CodeConfirmView, SendSMSVIew, CheckAuth

urlpatterns = [
    path('login/', SendSMSVIew.as_view(), name='login'),
    path('confirm/', CodeConfirmView.as_view(), name='code-confirm'),
    path('register/', RegistrationView.as_view(), name='registration'),
    path('logout/',  knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logout-all'),
    path('check/', CheckAuth.as_view(), name='check'),

    # path('login/', TokenObtainPairView.as_view(), name='login'),
    # path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    # path('first-register/', FirstRegistrationView.as_view(), name='first-register'),
    # path('last-register/', LastRegistrationView.as_view(), name='last-register'),

]
