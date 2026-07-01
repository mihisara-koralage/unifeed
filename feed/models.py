from django.db import models
from django.conf import settings
import re

class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)  # stored without the # symbol

    def __str__(self):
        return f'#{self.name}'

class Post(models.Model):
    author    = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    content   = models.TextField(max_length=1000)
    image     = models.ImageField(upload_to='post_images/', blank=True, null=True)
    hashtags  = models.ManyToManyField(Hashtag, blank=True, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # newest first

    def __str__(self):
        return f'{self.author.email} — {self.content[:40]}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._parse_hashtags()

    def _parse_hashtags(self):
        # Find every #word in the post content
        tags = re.findall(r'#(\w+)', self.content.lower())
        self.hashtags.clear()
        for tag in set(tags):  # set() removes duplicates
            hashtag, _ = Hashtag.objects.get_or_create(name=tag)
            self.hashtags.add(hashtag)

    @property
    def like_count(self):
        return self.likes.count()

    def is_liked_by(self, user):
        return self.likes.filter(user=user).exists()


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # one like per user per post

    def __str__(self):
        return f'{self.user.email} likes post {self.post.id}'