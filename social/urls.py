from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),  
    path('social-auth/', include('social_django.urls',namespace='social')),
]

if settings.DEBUG:
    urlpatterns =  urlpatterns  + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

    
    
