class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        # Calculate total post rating
        post_rating = (self.posts.aggregate(total_rating=Sum('post_rating'))['total_rating']) * 3 or 0

        # Calculate total comment rating
        comment_rating = self.comments.aggregate(total_rating=Sum('comment_rating'))['total_rating'] or 0

        # Calculate total rating of comments on posts authored by the author
        post_comments_rating = (
            sum(comment.comment_rating for post in self.posts.all() for comment in post.comments.all())
        )

        # Update user rating
        self.user_rating = post_rating + comment_rating + post_comments_rating
        self.save()