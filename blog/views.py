from django.contrib.auth.mixins import LoginRequiredMixin # new
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from .models import Post

class BlogListView(ListView):
    model = Post
    template_name = 'home.html'
    login_url = 'login'

class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    login_url = 'login'
class BlogCreateView(LoginRequiredMixin,CreateView):
    model = Post
    template_name = 'post_new.html'
    fields='__all__'
    login_url = 'login'
    def form_valid(self, form): # new
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogUpdateView(UpdateView):
    model = Post
    template_name = 'post_edit.html'
    fields = ['title', 'body']
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):  # new
        obj = self.get_object()

        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class BlogDeleteView(DeleteView):  # new
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')
    login_url = 'login'
    def dispatch(self, request, *args, **kwargs):  # new
        obj = self.get_object()

        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


