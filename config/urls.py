from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import home, send_push

from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Klinika 21 API",
        description="...",
        default_version="v1",
    ),
    public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('doctor/', include('doctor.urls')),
    path('docs/', schema_view.with_ui("swagger")),
    path('', home),
    path('send_push', send_push),
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/x-javascript'))
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




