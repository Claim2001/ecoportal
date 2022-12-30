from django.urls import path

from events.views_violation import ViolationCreateView, ViolationListView, ViolationRetrieveView, \
    ViolationUpdateDeleteView
from events.views_recycle import RecycleCreateView, RecycleListView, RecycleRetrieveView, RecycleUpdateDeleteView
from events.views_station import StationCreateView, StationListView, StationRetrieveView, StationUpdateDeleteView

urlpatterns = [
    path('violation/create/', ViolationCreateView.as_view(), name='violation-create'),
    path('violation/list/', ViolationListView.as_view(), name='violation-list'),
    path('violation/<int:id>/', ViolationRetrieveView.as_view(), name='violation-detail'),
    path('violation/change/<int:id>/', ViolationUpdateDeleteView.as_view(), name='violation-update-delete'),
    path('recycle/create/', RecycleCreateView.as_view(), name='recycle-create'),
    path('recycle/list/', RecycleListView.as_view(), name='recycle-list'),
    path('recycle/<int:id>/', RecycleRetrieveView.as_view(), name='recycle-detail'),
    path('recycle/change/<int:id>/', RecycleUpdateDeleteView.as_view(), name='recycle-update-delete'),
    path('station/create/', StationCreateView.as_view(), name='station-create'),
    path('station/list/', StationListView.as_view(), name='station-list'),
    path('station/<int:id>/', StationRetrieveView.as_view(), name='station-detail'),
    path('station/change/<int:id>/', StationUpdateDeleteView.as_view(), name='station-update-delete'),
]
