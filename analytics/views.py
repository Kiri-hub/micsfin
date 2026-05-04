from django.shortcuts import render, redirect, reverse, get_object_or_404


from .models import Student, Professor
from .forms import ProfessorForm


def homepage(request):
    students_qs = Student.objects.order_by("id")
    students_dict = {}

    for student in students_qs:
        courses = student.students_courses.all()
        students_dict[student.pk] = {
            'name': student.name,
            'surname': student.surname,
            'courses': courses,
            'professor': student.professor,
            'status': 'Active' if student.is_active else 'Not active'
        }

    return render(request, 'analytics/homepage.html', {'students': students_dict})


def view_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    courses = student.students_courses.all()

    return render(
        request,
        'analytics/view_student.html',
        {
            "student": student,
            "courses": courses,
            "total_income": student.get_total_income_from_student(),
            "school_rate": student.get_total_school_rate_from_student(),
            "professor_rate": student.get_total_professore_rate_from_student(),
        }
    )


def view_professors(request):
    professors_qs = Professor.objects.all()
    professors_dict = {}

    for professor in professors_qs:
        professors_dict[professor.pk] = {
            'name': professor.name,
            'surname': professor.surname,
            'picture': professor.picture,
            'pk': professor.pk,
        }

    return render(request, 'analytics/view_professors.html', {"professors": professors_dict})


def view_professor(request, pk):
    professor = get_object_or_404(Professor, pk=pk)

    total_income = professor.get_professor_total_income()
    professor_rate = professor.get_professor_total_rate()
    school_rate = professor.get_professor_total_school_rate()
    professor_students = professor.get_all_students()

    professor_dict = {
        "name": professor.name,
        "surname": professor.surname,
        "total_income": total_income,
        "professor_rate": professor_rate,
        "school_rate": school_rate,
        "professor_students": professor_students,
        "professor_students_num": len(professor_students),
        "professor_picture": professor.picture.url,
    }

    students = {}

    for student in professor_students:
        courses = student.students_courses.all()
        students[student.pk] = {
            'name': student.name,
            'surname': student.surname,
            'courses': courses,
            'professor': student.professor,
            'status': 'Active' if student.is_active else 'Not active',
            'total_income_from_student': student.get_total_income_from_student(),
            'professor_rate_from_student': student.get_total_professore_rate_from_student(),
            'school_rate_from_student': student.get_total_school_rate_from_student(),
        }

    return render(
        request,
        'analytics/view_professor.html',
        {
            'students': students,
            'professor': professor_dict
        }
    )


def view_school_profit(request):
    professors = Professor.get_all_professors()
    professors_dict = {}

    for professor in professors:
        total_income = professor.get_professor_total_income()
        professor_rate = professor.get_professor_total_rate()
        school_rate = professor.get_professor_total_school_rate()
        professor_students = professor.get_all_students()

        professors_dict[professor.pk] = {
            "name": professor.name,
            "surname": professor.surname,
            "total_income": total_income,
            "professor_rate": professor_rate,
            "school_rate": school_rate,
            "professor_students_num": len(professor_students),
        }

    context = {
        "professors": professors_dict,
        "total_income": Professor.get_all_professors_income(),
        "total_professors_rate": Professor.get_all_professors_rate(),
        "total_school_rate": Professor.get_total_school_rate(),
        "all_students": Student.len_all_students(),
    }

    return render(request, 'analytics/view_school_profit.html', context)


def create_student(request):
    return render(request, 'analytics/student_form.html')


def update_student(request, pk):
    return render(request, 'analytics/student_form.html')


def delete_student(request, pk):
    return render(request, 'analytics/homepage.html')


def create_professor(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('homepage'))
    form = ProfessorForm()
    return render(request, 'analytics/professor_form.html', {'form': form})



def export_students_excel(request):
    return render(request, 'analytics/homepage.html')