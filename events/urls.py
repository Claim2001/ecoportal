from django.urls import path

from events.views_violation import ViolationCreateView, ViolationListView, ViolationRetrieveView, \
    ViolationUpdateDeleteView

urlpatterns = [
    path('violation/create/', ViolationCreateView.as_view(), name='violation-create'),
    path('violation/list/', ViolationListView.as_view(), name='violation-list'),
    path('violation/<int:id>/', ViolationRetrieveView.as_view(), name='violation-get'),
    path('violation/change/<int:id>/', ViolationUpdateDeleteView.as_view(), name='violation-update-delete'),
]
