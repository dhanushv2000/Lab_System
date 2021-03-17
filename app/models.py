from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Section(models.Model):
    section = models.CharField(max_length = 200,null = True)
    faculty = models.ForeignKey(User, null=True, on_delete = models.CASCADE)

    def __str__(self):
        return self.section

class Student_link(models.Model):
    section = models.ForeignKey(Section, null=True, on_delete = models.CASCADE)
    roll_number = models.CharField(max_length = 200,null = True)
    email = models.CharField(max_length=400,null = True)

    def __str__(self):
        return self.roll_number
