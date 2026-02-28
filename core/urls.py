"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include
# --- ADD THESE IMPORTS ---
from django.conf import settings
from django.conf.urls.static import static
# -------------------------

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library.urls')),
    # library/urls.py
]

# This allows your browser to see the uploaded book images
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)