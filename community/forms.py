from django import forms
from django.forms import TextInput
from .models import Article, Article_Images, Comment, PrivateArticle

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
        fields = ('content',)

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')    
    class Meta:
        model = Article_Images
        fields = ('image', )


# class PrivateArticleForm(forms.ModelForm):

#     class Meta:
#         mdoel = PrivateArticle
#         fields = 'cotnent'

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