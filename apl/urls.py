from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from tasks import views

router = routers.DefaultRouter()
router.register(r'task', views.TaskView, basename='user')   
urlpatterns = router.urls
'''
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]'''
