from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/',views.Registerapi.as_view(), name='register'),
    path('login/',views.LoginView.as_view(), name='login'),
    path('todo/',views.Todoview.as_view(), name='todo'),
]
