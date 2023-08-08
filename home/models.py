from django.db import models

# Crea_te your models here.

class Color(models.Model):
    color_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.color_name


class Student(models.Model):
    # color = models.ForeignKey(Color, null=True, blank=True, on_delete=models.CASCADE , related_name="color")
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=18)
    father_name = models.CharField(max_length=100)
