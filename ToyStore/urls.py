"""
URL configuration for ToyStore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('store/', include('store.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from ToyStore import settings

app_name = 'ToyStore'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include("blog.urls")),
    path("store/", include("store.urls")),
    # path("auth/", include("authapp.urls")),
    path("", include("authapp.urls")),
    path("cart/", include("cart.urls")),
    path("financial/", include("financial.urls")),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
