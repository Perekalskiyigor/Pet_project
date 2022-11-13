from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('bboard.urls')),
    path('bboard/', include('bboard.urls')),
    path('admin/', admin.site.urls),
]
