"""
URL configuration for checkpoint_detection_app project.

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
from industrial_safety_app import views

urlpatterns = [
    path('checkpoint_detection_app/', views.index, name='index'),
    path('industrial_safety_app/', views.home, name='home'),
    path('success/', views.success, name='success'),  # URL for success page
    path('failure/', views.failure, name='failure'),  # URL for failure page
    path('process/', views.process, name='process'),  # URL for failure page
    path('inprogress/', views.inprogress, name='inprogress'),  # URL for failure page
    path('admin/', admin.site.urls),

]

if settings.DEBUG:  # Serve media files only in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)