from django.db import models


class Flags(models.Model):
    description = models.CharField(max_length=64, unique=True)
    continent = models.CharField(max_length=32, null=True)
    flag_base64 = models.BinaryField(null=True)


class Language(models.Model):
    language_code = models.CharField(max_length=2, primary_key=True)
    language_name = models.CharField(max_length=32)


class Translations(models.Model):
    country_name = models.ForeignKey(Flags, on_delete=models.CASCADE)
    translated_country_name = models.CharField(max_length=64)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)


class Audio(models.Model):
    country_name = models.ManyToManyField(Flags)
    language = models.ManyToManyField(Language)
    audio = models.BinaryField()


