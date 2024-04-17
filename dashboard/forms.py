from django import forms

from .models import Article


class AddArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'is_published', 'category', 'content', 'image_main')
        widgets = {
            'title': forms.Textarea(attrs={'cols': 80, 'rows': 1, 'class': 'form-control'}),
            'is_published': forms.CheckboxInput(),
            'category': forms.RadioSelect(choices=['PUBLIC', 'STAFF']),
            'content': forms.TextInput(attrs={'cols': 80, 'rows': 10, 'class': 'form-control'}),
            'image_main': forms.FileInput(attrs={'class': 'form-control'}),
        }
