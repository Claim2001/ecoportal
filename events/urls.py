from django.urls import path

from events.views import ViolationCreateView

urlpatterns = [
    path('violation/create/', ViolationCreateView.as_view(), name='violation-create'),
]
