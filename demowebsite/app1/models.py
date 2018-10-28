from django.db import models

# Create your models here.

class Message(models.Model):
    title = models.CharField(max_length=200)
    text  = models.TextField()

    def publish(self):
        self.save()

    def __str__(self):
        return self.title


class customer(models.Model):
    id = models.IntegerField(primary_key=True)
    emotion = models.CharField(max_length=10)