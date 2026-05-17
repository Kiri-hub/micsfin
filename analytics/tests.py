from django.test import TestCase
from django.urls import reverse

from .models import Student, Professor, ChessCourse


class PageTest(TestCase):

    def test_home_page_status(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_total_school_rate(self):
        professor = Professor.objects.create(
            name="Ivan"
        )

        course1 = ChessCourse.objects.create(
            course_price=100,
            professor_rate=40,
            per_lesson=False
        )

        course2 = ChessCourse.objects.create(
            course_price=200,
            professor_rate=50,
            per_lesson=False
        )

        student = Student.objects.create(
            name="John",
            surname="Doe",
            professor=professor
        )

        student.students_courses.add(course1)
        student.students_courses.add(course2)

        result = student.get_total_school_rate_from_student()

        self.assertEqual(result, 210)