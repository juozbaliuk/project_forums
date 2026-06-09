from .models import CustomUser, Post, Topic
from django import forms
from tinymce.widgets import TinyMCE
from django.contrib.auth.forms import UserCreationForm

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'photo']

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
        
class UserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'photo']