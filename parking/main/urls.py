from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from .views import get_parking_data

urlpatterns = [
    url(r'^parking/$', get_parking_data)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
