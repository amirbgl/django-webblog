from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404
from django.views import generic
from django.urls import reverse_lazy

from .models import Post
from .forms import PostForm


def post_list_view(request):
    posts_list = Post.objects.filter(status='pub').order_by("-datetime_modified")
    return render(request, 'blog/posts_list.html', {'posts_list' : posts_list})

def post_detail_view(request, pk):
    post =get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})

class PostCreateView(generic.CreateView):
    form_class = PostForm
    template_name = 'blog/post_create.html'

class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'

class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('posts_list')
