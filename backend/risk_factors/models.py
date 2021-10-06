from django.db import models


class Disease(models.Model):
    illness = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.illness


class Range(models.Model):
    min = models.PositiveSmallIntegerField(default=0)
    max = models.PositiveSmallIntegerField(default=10)

    def __str__(self):
        return f"[{self.min}..{self.max}]"


class Question(models.Model):
    description = models.TextField()
    label = models.CharField(max_length=100)
    range = models.ForeignKey(Range, on_delete=models.SET_NULL, null=True,
                              blank=True)

    def __str__(self):
        return self.description


class Option(models.Model):
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 related_name="options")
    answer = models.CharField(max_length=1000)

    def __str__(self):
        return self.answer
