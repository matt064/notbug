from django import forms

from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    "form to create or edit a blog post"
    class Meta:
        model = BlogPost
        fields = ['title', 'content']



