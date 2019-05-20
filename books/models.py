from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=250)
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE)
    annotation = models.TextField(blank=True)

    def __str__(self):
        return self.title
