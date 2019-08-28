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
    first_name = models.TextField(max_length=30, null=True, blank=True)
    last_name = models.TextField(max_length=30, null=True, blank=True)
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, related_name='profile')
    user_phone = models.CharField(max_length=140, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=191, null=False, blank=False)
    description = models.TextField(max_length=191, null=True, blank=True)
    body = models.TextField(null=False, blank=False)
    image = models.ImageField(upload_to='blog/%Y/%m/%d', null=True, blank=True)
    user = models.ForeignKey(DjangoUser, related_name='blog_posts', on_delete=models.CASCADE)
    published = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published',]




# class Comment(models.Model):
#     user = models.ForeignKey(DjangoUser)
#     post = models.ForeignKey(Post)
#     body = models.TextField()
#     created = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ('created',)
#
#     def __str__(self):
#         return 'Comment by {} on {}'.format(self.username, self.post)
