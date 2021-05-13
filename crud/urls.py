from django.urls import path
from .views import UserView, TokenView


app_name = "users"
urlpatterns = [
    path('users/', UserView.as_view()),
    path('users/<int:pk>', UserView.as_view()),
    path('api-token-auth/', TokenView.as_view())
    ]
