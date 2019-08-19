from django.urls import path
from . import views
from blog.views import ProfilePage

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:post_id>', views.details, name='details'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('post/delete/<int:post_id>/', views.post_delete, name='post_delete'),
    path('accounts/login/', views.user_login,  name='login'),
    path('accounts/logout/', views.user_logout, name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/<int:user_id>/edit/', views.profile_edit, name='profile_edit'),
    path('accounts/profile/', ProfilePage.as_view(), name='profile'),
    path('disciplines/', views.disciplines, name="disciplines"),
    path('history/', views.history, name="history")

]

