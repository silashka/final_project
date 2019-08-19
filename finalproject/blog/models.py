from django.db import models
from django.contrib.auth.models import User as DjangoUser


class User(models.Model):
    username = models.CharField(max_length=30, unique=True, error_messages={
        'unique': "A user with that username already exists."})
    first_name = models.TextField(max_length=30, null=True, blank=True)
    last_name = models.TextField(max_length=30, null=True, blank=True)
    password = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    user_phone = models.CharField(max_length=140, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class Post(models.Model):
    title = models.CharField(max_length=191, null=False, blank=False)
    description = models.TextField(max_length=191, null=True, blank=True)
    body = models.TextField(null=False, blank=False)
    image = models.FileField(null=True, blank=True)
    user = models.ForeignKey(DjangoUser, related_name='blog_posts', on_delete=models.CASCADE)
    published = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
