from django.contrib import admin
from .models import Actor, Movie, Comment, Account

admin.site.register(Actor)
admin.site.register(Movie)
admin.site.register(Comment)
admin.site.register(Account)
