from django.contrib import admin
from django.urls import path
from dietapp import views


urlpatterns = [
    path('list/', views.List),
    path('event/', views.Events),
    path('energy/', views.Energies),
    path('admin/', admin.site.urls),
]
