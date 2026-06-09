from django.db import models
from django.contrib.auth.models import AbstractUser
from tinymce.models import HTMLField
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to="profile_pics", null=True, blank=True)
    
    def count_posts(self):
        return Post.objects.filter(user=self.id).count()
    
class Task(models.Model):
    id = models.IntegerField(verbose_name="id", primary_key=True)
    name = models.CharField(verbose_name=_("Name"))
    content = HTMLField(verbose_name=_("Content"), max_length=3000, default="")
    user = models.ForeignKey(to='todo.CustomUser', verbose_name=_("User"), on_delete=models.SET_NULL, null=True, blank=True)
    datetime = models.DateTimeField(verbose_name=_("DateTime"), null=True, blank=True)
    
    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    def __str__(self):
        return f"{self.name}"
    
class Forum(models.Model):
    id = models.IntegerField(verbose_name="id", primary_key=True)
    name = models.CharField(verbose_name=_("Name"))
    description = models.CharField(verbose_name=_("Description"), null=True, blank=True)
    category = models.ForeignKey(to='Category', verbose_name=_("Category"), on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = _("Forum")
        verbose_name_plural = _("Forums")

    def __str__(self):
        return f"{self.name}"
    
    def get_topics(self):
        return Topic.objects.filter(forum=self.id).order_by("-pinned", "-id")
    
    def get_posts_count(self):
        topics = list(Topic.objects.filter(forum=self.id))
        count = 0
        for t in topics:
            count = count + Post.objects.filter(topic=t.id).count()
            
        return count
    
class Category(models.Model):
    id = models.IntegerField(verbose_name="id", primary_key=True)
    name = models.CharField(verbose_name=_("Name"))
    description = models.CharField(verbose_name=_("Description"), null=True, blank=True)
    staff_only = models.BooleanField(verbose_name=_("Staff Only"), default=False)
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return f"{self.name}"
    
    def get_forums(self):
        return Forum.objects.filter(category=self.id)
    
class Topic(models.Model):
    id = models.BigAutoField(verbose_name="id", primary_key=True)
    name = models.CharField(verbose_name=_("Name"))
    forum = models.ForeignKey(to='Forum', verbose_name=_("Forum"), on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(to='Tag')
    pinned = models.BooleanField(verbose_name="Pinned", default=False)
    locked = models.BooleanField(verbose_name="Locked", default=False)
    
    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")

    def __str__(self):
        return f"{self.name}"
    
    def get_tags(self):
        return "\n".join([t.name for t in self.tags.all()])
    
    def get_posts(self):
        return Post.objects.filter(topic=self.id)
    
    def get_first_post(self):
        return Post.objects.filter(topic=self.id).earliest("created_at")
    
    def get_last_post(self):
        return Post.objects.filter(topic=self.id).latest("created_at")
    
    def get_replies_count(self):
        return Post.objects.filter(topic=self.id).count() - 1
    
class Tag(models.Model):
    id = models.IntegerField(verbose_name="id", primary_key=True)
    name = models.CharField(verbose_name=_("Name"))
    description = models.CharField(verbose_name=_("Description"), null=True, blank=True)
    
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return f"{self.name}"

class Post(models.Model):
    id = models.BigAutoField(verbose_name="id", primary_key=True)
    user = models.ForeignKey(to='todo.CustomUser', verbose_name=_("User"), on_delete=models.SET_NULL, null=True, blank=True)
    topic = models.ForeignKey(to='Topic', verbose_name=_("Topic"), on_delete=models.CASCADE, null=True, blank=True)
    content = HTMLField(verbose_name=_("Content"), max_length=3000, default="")
    created_at = models.DateTimeField(verbose_name=_("Created At"), null=True, blank=True)
    last_edited = models.DateTimeField(verbose_name=_("Last Edited"), null=True, blank=True)
    
    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return f"{self.user} {self.topic}"