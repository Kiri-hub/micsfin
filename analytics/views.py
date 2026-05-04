import openpyxl
from openpyxl.styles import Font


from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


from datetime import datetime


from .models import Student, Professor
from .forms import ProfessorForm, StudentForm


def build_response(workbook):
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    filename = f"Учні_Мікс_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    workbook.save(response)
    return response


def export_students_excel(request):
    students = Student.objects.select_related("professor").prefetch_related("students_courses")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Students"

    write_headers(ws)
    write_students(ws, students)
    format_worksheet(ws)

    return build_response(wb)


def write_headers(ws):
    headers = [
        "Name", "Surname", "Active", "Professor",
        "Courses", "Total Income", "School Profit",
        "Professor Rate", "Notations",
    ]
    ws.append(headers)

    for cell in ws[1]:
        cell.font = Font(bold=True)


def write_students(ws, students):
    for student in students:
        courses = ", ".join(c.course_name for c in student.students_courses.all())

        ws.append([
            student.name,
            student.surname,
            "Yes" if student.is_active else "No",
            str(student.professor) if student.professor else "",
            courses,
            student.get_total_income_from_student(),
            student.get_total_school_rate_from_student(),
            student.get_total_professore_rate_from_student(),
            student.notations,
        ])


def format_worksheet(ws):
    for column in ws.columns:
        max_length = 0
        col_letter = column[0].column_letter

        for cell in column:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))

        ws.column_dimensions[col_letter].width = max_length + 2


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
def create_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("homepage"))
    form = StudentForm()
    return render(request, 'analytics/student_form.html', {"form": form, "action": "Create"})


@login_required
def update_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect(reverse("homepage"))
    form = StudentForm(instance=student)
    return render(request, 'analytics/student_form.html', {"form": form, "action": "Update"})


@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect(reverse("homepage"))


@login_required
def create_professor(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('homepage'))
    form = ProfessorForm()
    return render(request, 'analytics/professor_form.html', {'form': form})