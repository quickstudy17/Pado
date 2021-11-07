from django import forms
from django.forms import TextInput
from .models import Article, Comment

# class ArticleSelectForm(forms.ModelForm):

#     class Meta:
#         model = Article
#         fields = ('image',)


# class ArticleDetailForm(forms.ModelForm):

#     class Meta:
#         model = Article
#         fields = ('content',)


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('image', 'content',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': TextInput(attrs={
                'class': "form-control",
                'style': 'width: 400px;',
                'placeholder': '댓글 달기...'
            })
        }