from django.db import models
from django.conf import settings


class Continent(models.Model):
    name = models.CharField(max_length=32, null=True, unique=True)


class Flags(models.Model):
    flag_base64 = models.BinaryField(null=True)
    description = models.CharField(max_length=64, unique=True)


class Language(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=32)


class Country(models.Model):
    name = models.CharField(max_length=64)
    continent = models.ManyToManyField(Continent)
    flag = models.ForeignKey(Flags, on_delete=models.CASCADE)
    name_language = models.ForeignKey(Language, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                ('name'),
                ('name_language'),
                name='name_language_unique',
            ),
        ]

class Game(models.Model):
    name = models.CharField(max_length=64, null=True)

class Results(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, null=True, on_delete=models.CASCADE)
    result = models.SmallIntegerField(null=True)

    def __str__(self):
        return str(self.result)
    class Meta():
        ordering = ['result']


class Audio(models.Model):
    audio = models.BinaryField(null=True)
    country_name = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
