from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include
from rest_framework.authtoken import views

from adventure.api import ChamberViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register("chambers", ChamberViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/', include(router.urls)),
    path('api/adv/', include('adventure.urls')),
    path('api-token-auth/', views.obtain_auth_token)

]

