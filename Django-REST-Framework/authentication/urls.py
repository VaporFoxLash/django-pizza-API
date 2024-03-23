from django.urls import path
from . import views

urlpatterns = [
    path('', views.AuthView.as_view(), name='user_auth'),
    path('signup/', views.CreateUserView.as_view(), name='sign_up'),
]