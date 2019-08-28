from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .forms import LoginForm, RegistrationForm, PostForm, UserProfileForm
from blog.models import Post, UserProfile


def index(request):  # главная страница
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    # try:
    #     posts = paginator.page(page)
    # except PageNotAnInteger:
    #     posts = paginator.page(1)
    # except EmptyPage:
    #     posts = paginator.page(paginator.num_pages)

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


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        print(1)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published = datetime.now()
            post.save()
            print(2)
            return HttpResponseRedirect(reverse('details', kwargs={'post_id': post.id}))
            # return render(request, 'post/details.html', {'post': post})
    else:
        form = PostForm()
        print(3)
    return render(request, 'post/post_new.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    print(1)
    if request.method == "POST" and post.user.id == request.user.id:
        form = PostForm(request.POST, request.FILES, instance=post)
        print(2)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published = datetime.now()
            post.save()
            print(3)
        else:
            print(4)
            return HttpResponseRedirect(reverse('details', kwargs={'post_id': post.id}))
    else:

        form = PostForm(instance=post)
        print(5)
    return render(request, 'post/post_edit.html', {'form': form, 'post': post})


def post_delete(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST' and post.user.id == request.user.id:
        post.delete()
    return HttpResponseRedirect(reverse('index'))


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(request.POST)
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
            # return HttpResponseRedirect(reverse('register_done.html', kwargs={'new_user': new_user}))

            return render(request, 'accounts/register_done.html', {'new_user': new_user})
    else:
        user_form = RegistrationForm()
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('profile'))
    return render(request, 'accounts/registration.html', {'user_form': user_form})


class ProfilePage(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfilePage, self).get_context_data(**kwargs)
        profile = UserProfile.objects.get_or_create(user=self.request.user)[0]
        context['user_profile'] = profile
        context['user'] = self.request.user
        return context


@login_required  # изменение данных user
def profile_edit(request):
    form = None
    user = request.user
    user_profile = UserProfile.objects.filter(user__pk=user.id).first()
    if not user or not user_profile:
        pass  # to do add 404
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            if not User.objects.filter(username=request.POST.get('username')).exists():
                user.username = request.POST.get('username')
                user.save()
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'accounts/profile_edit.html', {'form': form, 'user': user, 'user_profile': user_profile})


# def comment(request, post_id):
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.user = request.user
#             comment.post = Post.objects.get(id=post_id)
#             form.save()
#         return


# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.POST, user=request.user)
#
#         if form.is_valid():
#             form.save()
#             update_session_auth_hash(request, form.user)
#             return redirect(reverse('profile'))
#         else:
#             return redirect(reverse('change_password'))
#     else:
#         form = PasswordChangeForm(user=request.user)
#
#         args = {'form': form}
#         return render(request, 'accounts/change_password.html', args)


# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)
#             return render(request, 'accounts/change_psw_done.html')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'accounts/change_password.html', {'form': form})


def disciplines(request):
    return render(request, 'blog/disciplines.html')


def history(request):
    return render(request, 'blog/history.html')
