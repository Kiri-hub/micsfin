from django.shortcuts import render, get_object_or_404
from .models import Student, Professor


def homepage(request):
    students = Student.objects.all()
    return render(request, 'analytics/homepage.html', {'students': students})


def view_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'analytics/view_student.html', {'student': student})


def view_professors(request):
    professors = Professor.objects.all()
    return render(request, 'analytics/view_professors.html', {'professors': professors})


def view_professor(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    students = professor.professor_students.all()

    return render(
        request,
        'analytics/view_professor.html',
        {
            'professor': professor,
            'students': students
        }
    )


def view_school_profit(request):
    professors = Professor.objects.all()
    students = Student.objects.all()

    context = {
        'professors': professors,
        'students': students,
    }

    return render(request, 'analytics/view_school_profit.html', context)