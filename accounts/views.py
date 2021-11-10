from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm

from .forms import CustomUserCreationForm
from community.models import Article

# Create your views here.
@require_http_methods(['GET', 'POST'])
def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('community:index')
        else:
            form = CustomUserCreationForm()
        context = {
            'form': form,
        }
        return render(request, 'accounts/signup.html', context)
    else:
        return redirect('community:index')


@require_http_methods(['GET', 'POST'])
def login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                user = form.get_user()
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect(request.GET.get('next') or 'community:index')
        else:
            form = AuthenticationForm()
        
        context = {
            'form': form,
        }
        return render(request, 'accounts/login.html', context=context)
    else:
        return redirect('community:index')


def logout(request):
    auth_logout(request)
    return redirect('community:index')


def profile(request, username):
    profile = get_object_or_404(get_user_model(), username=username)
    is_following = profile.followings.filter(pk=request.user.pk).exists()
    articles = Article.objects.filter(user_id=profile.id).order_by('-pk')
    context = {
        'profile': profile,
        'is_following': is_following,
        'articles': articles,
    }
    return render(request, 'accounts/profile.html', context)
    


def follow(request, username):
    following = request.user
    follower = get_object_or_404(get_user_model(), username=username)
    if following.followers.filter(pk=follower.pk).exists():
        following.followers.remove(follower)
    else:
        following.followers.add(follower)
    return redirect('accounts:profile', follower.username)


# def updateimg(request):
#     if not request.user.is_authenticated:
#         if request.method == 'POST':
#             form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
#             if form.is_valid():
#                 user = form.get_user()
#                 auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#                 return redirect(request.GET.get('next') or 'accounts:updateimg')
#         else:
#             form = CustomUserChangeForm(instance=request.user)
        
#         context = {
#             'form': form,
#         }
#         return render(request, 'accounts/login.html', context=context)
#     else:
#         return redirect('community:index')

