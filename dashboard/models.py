from django.db import models
from django.conf import settings

# Create your models here.
class Classroom(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    join_code = models.CharField(max_length=7)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class StudentClassroom(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    classroom = models.ForeignKey("Classroom", on_delete=models.CASCADE)

class TeacherClassroom(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    classroom = models.ForeignKey("Classroom", on_delete=models.CASCADE)

