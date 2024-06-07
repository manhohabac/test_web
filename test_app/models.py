from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=200)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Flashcard2(models.Model):
    question = models.TextField(max_length=255)
    answer = models.TextField(max_length=255)
    test = models.ForeignKey(Test, related_name='flashcards', on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return self.question


class UserScore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    objects = models.Manager()

    def __str__(self):
        return f"{self.user.name} - {self.score}"
