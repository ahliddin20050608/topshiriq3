from django.contrib import admin
from django.urls import path
from main.views import calculator

urlpatterns = [
    path('admin/', admin.site.urls),
    path('calc/', calculator), 
]

