from django import forms
from django.forms import ModelForm

from .models import Post

# class PostForm(forms.Form):
#     title = forms.CharField(label='title', max_length=50)
#     description = forms.CharField(label='description', max_length=200)

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description"] 