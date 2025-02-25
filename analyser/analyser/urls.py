"""
URL configuration for analyser project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from nexus.views import (
    AccountTransactionViewSet, 
    UploadFileView,  # ✅ Use UploadFileView instead of FileUploadView
    AnalyzeFileView  
)

# Create router for API endpoints
router = DefaultRouter()
router.register(r'transactions', AccountTransactionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Include API routes
    path('api/upload/', UploadFileView.as_view(), name='file-upload'),  # ✅ Update reference
    path('upload/', UploadFileView.as_view(), name='upload-file'),  # Additional upload processing endpoint
    path('api/analyze/', AnalyzeFileView.as_view(), name='file-analyze'),  # ✅ Add Analyze API
]

# ✅ Serve media files in development
def is_debug_mode():
    return getattr(settings, 'DEBUG', False)

if is_debug_mode():
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

