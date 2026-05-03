from django.db import models

from django.db import models


class Professor(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    picture = models.ImageField(upload_to="professors_pics/", null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.surname}"


class ChessCourse(models.Model):
    course_name = models.CharField(max_length=100)
    course_price = models.IntegerField()
    professor_rate = models.IntegerField()
    per_lesson = models.BooleanField(default=False)
    lessons_in_month = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.course_name


class Student(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    professor = models.ForeignKey(
        Professor,
        on_delete=models.CASCADE,
        null=True,
        related_name="students"
    )

    courses = models.ManyToManyField(
        ChessCourse,
        related_name="students"
    )

    notations = models.TextField(
        max_length=1000,
        default="Поки що немає нотаток",
        blank=True
    )

    def __str__(self):
        return f"{self.name} {self.surname}"