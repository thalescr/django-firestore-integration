from django.db import models

# Create your models here

"""
from django.contrib.auth import get_user_model

User = get_user_model()

class Certificate(models.Model):
    name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    emission_date = models.DateField()
    credential_code = models.CharField(max_length=255, null=True, blank=True)
    credential_url = models.URLField(null=True, blank=True)

class Skill(models.Model):
    SKILL_LEVEL_CHOICES = (
        ('Aprendiz', 0),
        ('Básico', 1),
        ('Intermediário', 2),
        ('Avançado', 3),
        ('Expert', 4)
    )
    name = models.CharField(max_length=255)
    skill_level = models.IntegerField(choices=SKILL_LEVEL_CHOICES)

"""