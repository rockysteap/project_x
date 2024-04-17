from django import forms

from .models import Article


class AddArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'is_published', 'category', 'content', 'image_main')
        widgets = {
            'title': forms.TextInput(),
            'is_published': forms.BooleanField(),
            'category': forms.Select(),
            'content': forms.Textarea(),
            'image_main': forms.FileInput(),
        }
