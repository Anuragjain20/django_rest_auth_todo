from django.urls import path
from .views import *

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'todo', TodoView)

urlpatterns = [
    path("",test,name = "test"),

]
urlpatterns += router.urls