from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import (
    MovieViewSet,
    ActorVievSet,
    MovieActorAPIView,
    CommentDelete,
    CommentListCreate,
    registration_view,
    )

#from .views import CommentPost, CommentGet,
router = DefaultRouter()

router.register('movies', MovieViewSet)
router.register('actors', ActorVievSet)

# editor.swagger.io

app_name = 'account'

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', views.obtain_auth_token),
    path('register/', registration_view, name='register'),
    path('movie/<int:pk>/actors', MovieActorAPIView.as_view(), name="actor"),
    path('comments/', CommentListCreate.as_view(), name="comments"),
    path('comments/delete/', CommentDelete.as_view(), name="delete"),
    # path('comment/',CommentPost.as_view(), name="comment"),
    # path('comments/', CommentGet.as_view(), name="comments"),
]
