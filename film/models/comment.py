from django.contrib.auth import get_user_model
from django.db import models
from .movie import Movie

User = get_user_model()


class Comment(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=512)
    created_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'Comment'

    def __str__(self):
        return self.text


