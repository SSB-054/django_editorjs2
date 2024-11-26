from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'django_editorjs2_blog/post_form.html'

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'django_editorjs2_blog/post_form.html'

class PostDetailView(DetailView):
    model = Post
    template_name = 'django_editorjs2_blog/post_detail.html'

class PostListView(ListView):
    model = Post
    template_name = 'django_editorjs2_blog/post_list.html'