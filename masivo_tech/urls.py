from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('marketplace.urls')),
    path('soporte/', include('chat.urls')),
    path('accounts/', include('allauth.urls')),  # necesario para allauth
    path('accounts/', include('users.urls')), # usuarios
]

# Debug Toolbar - SOLO EN DESARROLLO
if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass

# ⚠️ IMPORTANTE: Las rutas static() deben ir DESPUÉS de todo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)