from home.views import *
from django.urls import path,include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='students')
urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('register/',RegisterAPI.as_view()),
    path('login-api/', LoginAPI.as_view()),
    path('logout-api/', LogoutAPI.as_view()),
    path('student-api/', StudentAPI.as_view()),
    path('student/',student)
]

