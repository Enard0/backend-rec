from django.urls import include, path
from rest_framework import routers
from tasks import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'regist', views.RegisterViewSet, basename='regist')
router.register(r'tasks', views.TaskViewSet, basename='task')
router.register(r'history', views.HistoryViewSet, basename='history')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]