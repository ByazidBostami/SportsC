from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bookings.urls')),  # Your app's URLs
    path('accounts/', include('django.contrib.auth.urls')),
]
