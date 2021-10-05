from django.db import models


class Disease(models.Model):
    illness = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.illness
