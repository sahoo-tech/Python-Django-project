from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list_view, name='blog_list'),
    path('post/<slug:slug>/', views.blog_detail_view, name='blog_detail'),
    path('my-posts/', views.my_posts_view, name='my_posts'),
    path('create/', views.blog_create_view, name='blog_create'),
    path('update/<slug:slug>/', views.blog_update_view, name='blog_update'),
    path('delete/<slug:slug>/', views.blog_delete_view, name='blog_delete'),
]
