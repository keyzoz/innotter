from django.db import models

# Create your models here.


class Followers(models.Model):
    page_id = models.ForeignKey(
        "page.Page", on_delete=models.CASCADE, related_name="follow_page"
    )
    user = models.CharField()


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class Page(models.Model):

    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    image_url = models.URLField(null=True, blank=True)
    user = models.CharField()
    tags = models.ManyToManyField(Tag, related_name="tags")
    followers = models.ManyToManyField(
        Followers,
        related_name="followers",
        blank=True,
    )
    is_blocked = models.BooleanField(default=False)
    unblock_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.name
