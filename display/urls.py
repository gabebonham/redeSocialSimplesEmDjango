from django.urls import path
from . import views
from posts.models import Post

urlpatterns = [
    path('', views.index,name="index"),
    path('cadastro/', views.cadastro,name='cadastro'),
    path('loginUser/', views.loginUser,name="loginUser"),
    path('createUser/', views.createUser,name="createUser"),
    path("socialMedia/", views.socialMedia,name="socialMedia"),
    path('post/', views.post, name="post"),
    path('createPost/',views.createPost,name="createPost"),
    path("posts/<slug:slug>", views.selectedPost, name="selectedPost"),
    path("posts/<slug:slug>/addLike", views.addLike, name="addLike"),
    path("logout", views.logoutSystem, name="logoutSystem"),
    path("createComment", views.createComment, name="createComment")
]