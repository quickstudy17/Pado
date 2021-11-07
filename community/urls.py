from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.index, name='index'),
    # 게시판 C
    path('create/select/', views.create_select, name='create_select'),
    path('create/detail/', views.create_detail, name='create_detail'),
    path('create/upload/', views.create_upload, name='create_upload'),
    # 게시판 R
    path('<int:article_pk>/', views.detail, name='detail'),
    # 게시판 D
    path('<int:article_pk>/delete/', views.article_delete, name='article_delete'),
    # 게시판 좋아요
    path('<int:article_pk>/like/', views.article_like, name='article_like'),

    # 댓글 C
    path('<int:article_pk>/comments/create/', views.comment_create, name='comment_create'),
    # 댓글 D
    path('<int:article_pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    # 댓글 좋아요
    path('<int:article_pk>/comments/<int:comment_pk>/like/', views.comment_like, name='comment_like'),
    
    # 검색
    path('search/', views.search, name='search'),
]
