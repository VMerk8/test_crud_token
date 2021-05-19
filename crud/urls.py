from django.urls import path, include
from .views import UserView, TokenView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserView)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-token-auth/', TokenView.as_view())
]
