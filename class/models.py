from django.db import models

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
