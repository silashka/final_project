from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import TemplateView
from .forms import LoginForm, RegistrationForm, PostForm, UserProfileForm
from .models import Post, UserProfile
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def index(request):  # главная страница
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'post/list.html', context)

@login_required
def details(request, post_id):  # страница для чтения отдельного поста
    posts = get_object_or_404(Post, pk=post_id)
    context = {
        'post': posts,
    }
    return render(request, 'post/details.html', context)


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published = datetime.now()
            post.save()
            return render(request, 'post/details.html', {'post': post})
    else:
        form = PostForm()
    return render(request, 'post/post_new.html', {'form': form})

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST" and post.user.id == request.user.id:
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published = datetime.now()
            post.save()
            return HttpResponseRedirect(reverse('details', kwargs={'post_id': post.id}))
    else:
        form = PostForm(instance=post)
    return render(request, 'post/post_edit.html', {'form': form, 'post': post})


def post_delete(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST' and post.user.id == request.user.id:
        post.delete()
    return HttpResponseRedirect(reverse('index'))


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('profile'))
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        print(request.POST.get('prev_page'))
        return HttpResponseRedirect(request.POST.get('prev_page'))


def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            return render(request, 'accounts/register_done.html', {'new_user': new_user})
    else:
        user_form = RegistrationForm()
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('profile'))
    return render(request, 'accounts/registration.html', {'user_form': user_form})


class ProfilePage(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def check_user(self, user):
        if user.is_active:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(ProfilePage, self).get_context_data(**kwargs)
        profile = UserProfile.objects.get_or_create(user=self.request.user)[0]
        context['profile'] = profile
        return context


@login_required  # изменение данных user
def profile_edit(request, user_id):
    form = None
    try:
        user = UserProfile.objects.filter(user__pk=user_id)
        if request.method == 'POST':
            form = UserProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                context = {
                    'user_id': user_id
                }

                return render(request, 'accounts/profile.html', context)
        else:
            form = UserProfileForm(instance=request.user)
    except UserProfile.DoesNotExist:
        pass
    return render(request, 'accounts/profile_edit.html', {'form': form})


# def save_profile(request):  # сохранение данных user
#     if request.method == 'POST':
#         user = UserProfile()
#         user.username = request.POST.get('username')
#         user.email = request.POST.get('email')
#         user.birth_date = request.POST.get('birth_date')
#         user.save()
#     return HttpResponseRedirect("/")


def disciplines(request):
    return render(request, 'blog/disciplines.html')


def history(request):
    return render(request, 'blog/history.html')
