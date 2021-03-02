from django.db import models
from django.conf import settings
from datetime import date
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, 
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True, 
                                     default='1990-01-26')
    
    def __str__(self):
        return f'Profile for user {self.user.username}'


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique_for_date='publish',
                            allow_unicode=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, 
                                related_name='author_posts')
    body = models.TextField(max_length=2000)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='published')
    
    objects = models.Manager()
    published = PublishedManager()
    liked = models.ManyToManyField(User, default=None, blank=True, related_name='liked')

    @property
    def num_likes(self):
        return self.liked.all().count()

    class Meta:
        ordering = ('-publish',)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.publish.year,
                                            self.publish.month,
                                            self.publish.day, self.slug])
    


class Comment(models.Model):
    post = models.ForeignKey(Post, 
                            on_delete=models.CASCADE,
                            related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                            related_name='author_comments')
    body = models.TextField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    liked = models.ManyToManyField(User, default=None, blank=True, related_name='comment_liked')
    
    @property
    def num_likes(self):
        return self.liked.all().count()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'



class Like(models.Model):
    LIKE_CHOICES = (
        ('Like', 'Like'),
        ('Unlike', 'Unlike'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.post)


class CommentLike(models.Model):
    LIKE_CHOICES = (
        ('Like', 'Like'),
        ('Unlike', 'Unlike'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.comment)