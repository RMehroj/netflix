from django.db import models
from .actor import Actor
from django.core.validators import MinValueValidator, MaxValueValidator


class Movie(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    year = models.DateField(auto_now=True, blank=True)
    imdb = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    genre = models.CharField(max_length=256, blank=False, null=False)
    actor = models.ManyToManyField(Actor)

    class Meta:
        db_table = 'Movie'

    def __str__(self):
        return self.name