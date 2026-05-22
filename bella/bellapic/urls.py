from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_landing, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('post/like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('post/comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('comment/reply/<int:comment_id>/', views.add_reply, name='add_reply'),
]
