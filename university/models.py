from django.db import models


class Lecturer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    credits = models.IntegerField()
    lecturer = models.ForeignKey(
        Lecturer,
        on_delete=models.CASCADE,
        related_name='courses'
    )

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    student_id = models.CharField(max_length=20, unique=True)
    courses = models.ManyToManyField(Course, related_name='students')

    def __str__(self):
        return self.name
