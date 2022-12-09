from django.conf.urls.static import static
from django.contrib import admin
from ecoportal import settings
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(title="Ecoportal API", default_version='v1', description="Ecoportal urls",
                 contact=openapi.Contact(email="https://t.me/Yourtoughmango"),
                 license=openapi.License(name="Ecoportal License")),
    public=True, permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('account/', include(('account.urls', 'account'), namespace='account')),
    path('events/', include(('events.urls', 'events'), namespace='events')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
