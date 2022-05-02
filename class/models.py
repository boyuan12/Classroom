from django.db import models
from django.conf import settings


# Create your models here.
class Assignment(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    classroom = models.ForeignKey("dashboard.Classroom", on_delete=models.CASCADE)
    points = models.IntegerField()
    assigned = models.DateField(auto_now=True)
    due = models.DateTimeField(null=True)
    slug = models.SlugField()

class Topic(models.Model):
    classroom = models.ForeignKey("dashboard.Classroom", on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

class File(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Submission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    files = models.ForeignKey(File, null=True, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    text = models.TextField(null=True)
