from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_safe, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required

from .models import Article, Comment
from accounts.models import User
from .forms import ArticleForm, CommentForm

# Create your views here.
def index(request):
    articles = Article.objects.order_by('-pk')
    form = CommentForm()
    context = {
        'articles': articles,
        'form': form,
    }
    return render(request, 'community/index.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create_select(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('community:index')
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'community/create_select.html', context)


def create_detail(request):
    pass


def create_upload(request):
    pass


def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    form = CommentForm()
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'community/detail.html', context)


@require_POST
def article_delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user.is_authenticated:
        if request.user == article.user:
            article.delete()
            return redirect('community:index')
    return redirect(request.META.get('HTTP_REFERER'))


def article_like(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if article.like_users.filter(pk=request.user.pk).exists():
        article.like_users.remove(request.user)
    else:
        article.like_users.add(request.user)
    return redirect(request.META.get('HTTP_REFERER'))


def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.user = request.user
        comment.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
@require_POST
def comment_delete(request, article_pk, comment_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def comment_like(request, article_pk, comment_pk):
    pass


def search(request):
    users = User.objects.all()
    articles = Article.objects.order_by('-pk')
    q = request.POST.get('q', "")

    if q[0] == '#':
        articles = articles.filter(content__contains=q[1:])
        context = {
            'articles': articles,
            'q': q,
        }
        return render(request, 'community/search.html', context)
    elif q:
        users = users.filter(username__icontains=q)
        context = {
            'users': users,
            'q': q,
        }
        return render(request, 'community/search.html', context)
    else:
        return render(request, 'community/search.html')
