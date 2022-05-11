from django.db import models


class Account(models.Model):
    email = models.EmailField(max_length=256, blank=False, null=False)
    username = models.CharField(max_length=256, blank=False, null=False)
    password = models.CharField(max_length=256, blank=False, null=False)

    class Meta:
        db_table = 'Account'

    def __str__(self):
        return self.username