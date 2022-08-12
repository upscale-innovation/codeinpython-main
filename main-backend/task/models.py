from django.db import models

# Create your models here.
from datetime import datetime
from account.models import *

from django.utils.text import slugify
import random
import string
from django.utils.timezone import now

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

POST_STATUS = (('is_open', 'is_open'), ('is_closed', 'is_closed'))
class Post(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(max_length=1000, blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=now)
    updated_on = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, max_length = 100)
    is_edited = models.BooleanField(default=False)
    post_status	= models.CharField(max_length=10, blank=False, null=True, choices=POST_STATUS, default='is_open')

    def unique_slug_generator(instance, new_slug=None):
        if new_slug is not None:
            slug = new_slug
        else:
            slug = slugify(instance.title)

        Klass = instance.__class__
        qs_exists = Klass.objects.filter(slug=slug).exists()
        if qs_exists:
            new_slug = "{slug}-{randstr}".format(
                        slug=slug,
                        randstr=random_string_generator(size=4)
                    )
            return unique_slug_generator(instance, new_slug=new_slug)
        return slug


class PostFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=False)
    file = models.FileField(blank=True, null=True)
    created_on = models.DateTimeField(default=now)

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=False)
    image = models.ImageField(blank=True, null=True)
    created_on = models.DateTimeField(default=now)

class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_by')
    created_on = models.DateTimeField(default=now)

    class Meta:
        unique_together = ('post', 'liked_by')


class PostBookmark(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_bookmark')
    bookmark_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmark_by')
    created_on = models.DateTimeField(default=now)

    class Meta:
        unique_together = ('post', 'bookmark_by')