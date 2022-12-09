from django.urls import path
from knox import views as knox_views

from account.views import RegistrationView, CodeConfirmView, SendSMSView

urlpatterns = [
    path('login/', SendSMSView.as_view(), name='login'),
    path('confirm/', CodeConfirmView.as_view(), name='code-confirm'),
    path('register/', RegistrationView.as_view(), name='registration'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logout-all'),
]
