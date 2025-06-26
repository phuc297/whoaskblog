import json
from django import forms
from django_quill.widgets import QuillWidget

from django.conf import settings

from apps.posts.models import Post, Tag


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-xl px-4 py-2 focus:outline-none focus:ring-1 focus:ring-green-500',
                'placeholder': 'Nhập tag và nhấn Enter',
                'name': "tag_form"
            })
        }


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content', 'description',
                  'category', 'thumbnail')
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
                'class': 'w-full text-gray-700 bg-white px-4 py-2 border border-gray-200',
            })
        }
