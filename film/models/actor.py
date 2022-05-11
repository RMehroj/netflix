from django.db import models
GENDER_MALE = 0
GENDER_FEMALE = 1
GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female')]


class Actor(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    birthdate = models.DateField(null=True, blank=True,)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=0)

    class Meta:
        db_table = 'Actor'

    def __str__(self):
        return self.name
