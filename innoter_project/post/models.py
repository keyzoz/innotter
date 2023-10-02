from django.db import models


class Likes(models.Model):
    post_id = models.ForeignKey(
        "post.Post", on_delete=models.CASCADE, related_name="liked_post"
    )
    user_id = models.IntegerField()


class Post(models.Model):

    page = models.ForeignKey(
        "page.Page",
        on_delete=models.CASCADE,
    )

    content = models.TextField()

    reply_to = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="replies"
    )

    likes = models.ManyToManyField(Likes, blank=True, related_name="likes")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
