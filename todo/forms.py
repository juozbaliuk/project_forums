from .models import CustomUser, Post, Topic
from django import forms
from tinymce.widgets import TinyMCE
from django.contrib.auth.forms import UserCreationForm

class UserChangeForm(forms.ModelForm):
    flair = forms.CharField(widget=TinyMCE())
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'photo', 'flair']

class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        
class PostForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE())
    class Meta:
        model = Post
        fields = ['content']
        
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name']