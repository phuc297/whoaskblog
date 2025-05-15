import json
from django import forms
from django_quill.widgets import QuillWidget

from django.conf import settings

from apps.posts.models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content', 'description', 'category', 'thumbnail')
        widgets = {
            'title': forms.TextInput(attrs={
                'rows': 4,
                'cols': 40,
                'class': 'w-full bg-white text-gray-700 border border-gray-200 focus:outline-none px-4 py-2 text-4xl min-h-15',
                'placeholder': 'Tiêu đề...',
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'cols': 40,
                'class': 'w-full bg-white text-gray-700 border border-gray-200 focus:outline-none px-4 py-2 text-lg',
                'placeholder': 'Mô tả...',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full bg-white text-gray-700 border border-gray-200 focus:outline-none px-4 py-2',
            }),
            'thumbnail': forms.ClearableFileInput(attrs={
                'class': 'w-full text-gray-700 bg-white px-4 py-2 border border-gray-200 ql-editor',
            }),
        }
