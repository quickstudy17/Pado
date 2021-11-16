import random
import os.path

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_safe, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .models import Article, Comment, Article_Images
from accounts.models import User
from .forms import ArticleForm, CommentForm, ImageForm, PrivateArticleForm
from django.contrib.auth.models import Group
from django.forms import modelformset_factory

from PIL import Image

# Create your views here.
def index(request):
    articles = Article.objects.order_by('-pk')
    page = request.GET.get('page', '1')
    paginator = Paginator(articles, '10')
    page_obj = paginator.get_page(page)
    form = CommentForm()
    context = {
        'articles': page_obj,
        'form': form,
    }
    return render(request, 'community/index.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create_select(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid() :
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            image_list = request.FILES.getlist('image')
            for image in image_list:
                image = Image.objects.create(image=image, article_id=article.pk)
            return HttpResponseRedirect("/")
    else:
        form = ArticleForm()
    context = {
        'form': form,
 
    }
    return render(request, 'community/create_select.html', context)

# @login_required
# @require_http_methods(['GET', 'POST'])
# def create_private_article(request):
#     if request.method == 'POST':
#         form = PrivateArticleForm(request.POST)
#         if form.is_valid():
#             private_article = form.save(commit=False)
#             private_article.user = request.user
#             user = request.user
#             private_article.save()
#             new_group = Group.objects.create(name= private_article.pk)
#             user.groups.add(new_group)
#             return redirect('community:index_private', private_article.pk)
#     else:
#         private_article_form = PrivateArticleForm()
#     context = {
#         'private_article_form' : private_article_form,
#     }
#     return redirect('comunity:index')


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

@login_required
@require_http_methods(['GET', 'POST'])
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user == article.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                return redirect('community:detail', article.pk)
        else:
            form = ArticleForm(instance=article)
    else:
        return redirect('articles:index')
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'community/update.html', context)


@require_POST
def article_delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user.is_authenticated:
        if request.user == article.user:
            article.delete()
            return redirect('community:index')
    return redirect(request.META.get('HTTP_REFERER'))


def article_like(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)

        # 현재 좋아요를 요청하는 회원(request.user)이
        # 해당 게시글의 좋아요를 누른 회원 목록에 이미 있다면,
        if article.like_users.filter(pk=request.user.pk).exists():
            # 좋아요 취소
            article.like_users.remove(request.user)
            liked = False
        else:
            # 좋아요 하기
            article.like_users.add(request.user)
            liked = True

        like_count = article.like_users.count()
        context = {
            'liked' : liked,
            'like_count' : like_count,
        }
        return JsonResponse(context)


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


@require_POST
def zoom_img(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    image = Image.open(article.image)
    zoom = random.uniform(0.7, 1.3)
    width, height = image.size
    x = width / 2
    y = height / 2
    crop_image = image.crop((x - (width / 2 / zoom), y - (height / 2 / zoom), x + (width / 2 / zoom), y + (height / 2 / zoom)))
    zoom_image = crop_image.resize((width, height), Image.LANCZOS)
    save_path = './static/'
    zoom_image.save(os.path.join(save_path, 'zoom_image.png'))   

    context = {
        'zoom_image':zoom_image,
        'article':article,
    }
    return render(request, 'community/zoom.html', context)    
