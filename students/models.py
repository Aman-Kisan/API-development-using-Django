from django.db import models

# Create your models here.

class Student(models.Model):
    reg_no = models.IntegerField(primary_key=True,blank=False)
    name = models.CharField(max_length=200,blank=False)
    branch = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    