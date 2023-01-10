from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('project_app.urls')),
    path('bot/', include('django_telegram.urls', namespace='bot')),
    path('admin/', admin.site.urls),
]
