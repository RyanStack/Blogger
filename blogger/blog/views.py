from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.core.urlresolvers import reverse
from .models import Post
from .forms import PostForm

class PostList(ListView):
    template_name = 'blog/list.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        return Post.objects.order_by('-created_date')[:10]

class PostDetails(DetailView):
    model = Post
    template_name = 'blog/details.html'

class PostCreate(CreateView):
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.created_date = timezone.now()
        return super(PostCreate, self).form_valid(form)

class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/update.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'blog/delete.html'
    
    def get_success_url(self):
        return reverse('blog:list')

