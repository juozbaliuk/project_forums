from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic.edit import FormMixin
from .models import Task, Forum, Category, Topic, Post
from django.urls import reverse, reverse_lazy
from .forms import CustomUserCreateForm, PostForm, TopicForm, UserChangeForm
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.db.models import Q

# Create your views here.
# def index(request):
#     return render(request, template_name="index.html")
    
class TaskListView(generic.ListView):
    model = Task
    template_name = "tasks.html"
    context_object_name = "tasks"
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
class TaskDetailView(generic.DetailView):
    model = Task
    template_name = "task.html"
    context_object_name = "task"
    
class SignUpView(generic.CreateView):
    form_class = CustomUserCreateForm
    template_name = "signup.html"
    success_url = reverse_lazy("login")
    
class CategoryListView(generic.ListView):
    model = Category
    template_name = "index.html"
    context_object_name = "categories"

def forum(request, forum_id):
    forum = Forum.objects.get(pk=forum_id)
    topics = Topic.objects.filter(forum=forum_id)
    posts = []
    for t in topics:
        posts.append(Post.objects.filter(topic=t).first())
        
    posts.sort(key=lambda x: x.created_at, reverse=True)
    posts.sort(key=lambda x: x.topic.pinned, reverse=True)
    
    topics = []
    for p in posts:
        topics.append(Topic.objects.filter(forum=forum_id).filter(pk=p.topic.id).first())
    
    paginator = Paginator(topics, per_page=20)
    page_number = request.GET.get('page')
    paged_topics = paginator.get_page(page_number)
    context = {
        'topics': paged_topics,
        'forum': forum,
    }
    return render(request, template_name="forum.html", context=context)
    
class PostsListView(FormMixin, generic.ListView):
    model = Post
    template_name = "topic.html"
    context_object_name = "posts"
    form_class = PostForm
    paginate_by = 10
    
    def get_success_url(self):
        return reverse("topic", kwargs={"pk": self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = Topic.objects.filter(pk=self.kwargs['pk']).first()
        form = self.get_form()
        if form.is_valid() and not self.object.locked:
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.topic = Topic.objects.filter(pk=self.kwargs['pk']).first()
        form.instance.user = self.request.user
        form.instance.created_at = datetime.now()
        form.save()
        
        return super().form_valid(form)
    
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(topic=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topic"] = Topic.objects.filter(pk=self.kwargs['pk']).first()
        return context

class NewTopicView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Forum
    form_class = TopicForm
    second_form_class = PostForm
    template_name = "new_topic.html"
    
    def get_success_url(self):
        return reverse("topic", kwargs={"pk": self.object.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "second_form" not in context:
            context["second_form"] = self.second_form_class()
        return context

    def post(self, request, *args, **kwargs):
        topic_form = self.get_form()
        post_form = self.second_form_class(request.POST)
        if topic_form.is_valid() and post_form.is_valid():
            return self.forms_valid(topic_form, post_form)
        # if either form invalid, render page with errors
        return self.render_to_response(self.get_context_data(form=topic_form, secondary_form=post_form))

    def forms_valid(self, topic_form, post_form):
        topic_form.instance.forum = Forum.objects.get(id=self.kwargs["pk"])
        topic_form.save()
        
        post_form.instance.topic = topic_form.instance
        post_form.instance.user = self.request.user
        post_form.instance.created_at = datetime.now()
        post_form.save()

        self.object = topic_form.instance
        return HttpResponseRedirect(self.get_success_url())
    
    def test_func(self):
        return self.get_object().category.staff_only and self.request.user.is_staff or not self.get_object().category.staff_only
    
class SettingsUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = UserChangeForm
    template_name = "settings.html"
    success_url = reverse_lazy('settings')

    def get_object(self, queryset=None):
        return self.request.user
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = "post_update.html"
    
    def get_success_url(self):
        return reverse("topic", kwargs={"pk": self.object.topic.id})
    
    def form_valid(self, form):
        form.instance.last_edited = datetime.now()
        form.save()
        
        return HttpResponseRedirect(self.get_success_url())
    
    def test_func(self):
        return self.get_object().user == self.request.user and not self.get_object().topic.locked
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = "post_delete.html"
    context_object_name = "post"
    # success_url = reverse_lazy('orders')

    def get_success_url(self):
        return reverse("topic", kwargs={"pk": self.get_object().topic.id})
    
    def form_valid(self, form):
        post = self.get_object()
        if Post.objects.filter(topic=post.topic).first() == post:
            forum = post.topic.forum
            post.topic.delete()
            return redirect('forum', forum.id)
        return super().form_valid(form)
    
    def test_func(self):
        return (self.get_object().user == self.request.user or self.request.user.is_staff) and not self.get_object().topic.locked
    
def search(request):
    query = request.GET.get('query')

    post_search_results = Post.objects.filter(
        Q(content__icontains=query) | Q(user__username__iexact=query) | Q(topic__name__icontains=query)
    ).order_by("-created_at")

    paginator = Paginator(post_search_results, per_page=10)
    page_number = request.GET.get('page')
    paged_posts = paginator.get_page(page_number)

    context = {
        "query": query,
        "posts": paged_posts,
    }
    
    return render(request, template_name="search.html", context=context)