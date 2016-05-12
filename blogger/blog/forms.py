from django import forms
from django.forms import ModelForm, Textarea

from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description"] 
        widgets = {
            'title': Textarea(attrs={'cols': 80, 'rows': 20}),
            'description': Textarea(attrs={'cols': 80, 'rows': 20}),
        }