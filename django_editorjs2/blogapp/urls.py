from django.urls import path
from .views import PostCreateView, PostUpdateView, PostDetailView, PostListView

app_name = 'django_editorjs2_blogapp'
urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('new/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
]