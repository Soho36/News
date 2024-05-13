from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        # Calculate total post rating
        post_rating = (
                Post.objects.filter(author=self).aggregate(total_rating=Sum('post_rating'))['total_rating']
                or 0
        )
        post_rating *= 3  # Multiply by 3 as per your adjustment

        # Calculate total comment rating
        comment_rating = (
                Comment.objects.filter(user=self.user).aggregate(total_rating=Sum('comment_rating'))['total_rating']
                or 0
        )

        # Calculate total rating of comments on posts authored by the author
        post_comments_rating = (
                Comment.objects.filter(post__author__user=self.user).aggregate(total_rating=Sum('comment_rating'))
                ['total_rating'] or 0
        )

        # Update user rating
        self.user_rating = post_rating + comment_rating + post_comments_rating
        self.save()


class Post(models.Model):
    objects = models.Manager()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
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
        return beginning_of_article


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    objects = models.Manager()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
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




