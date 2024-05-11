from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def like_dislike(self, like):
        if like:
            self.user_rating += 1
        elif int(self.user_rating) > 0:  # Ensure rating doesn't go negative
            self.user_rating -= 1
        self.save()

    def update_rating(self):
        pass

class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    article_or_news = models.BooleanField(default=False)        # True for Article, False for News
    creation_time = models.DateTimeField(auto_now_add=True)     # Post creation time
    category = models.ManyToManyField(Category, through='PostCategory')
    post_header = models.CharField(max_length=255)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def like_dislike(self, like):
        if like:
            self.post_rating += 1
        elif int(self.post_rating) > 0:  # Ensure rating doesn't go negative
            self.post_rating -= 1
        self.save()

    def preview(self):
        beginning_of_article = self.post_text[:124] + ' ...'
        self.save()
        return beginning_of_article


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like_dislike(self, like):
        if like:
            self.comment_rating += 1
        elif int(self.comment_rating) > 0:  # Ensure rating doesn't go negative
            self.comment_rating -= 1
        self.save()
