from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name="homepage"),

    path('professors/', views.view_professors, name="view_professors"),
    path('professor/<int:pk>/', views.view_professor, name="view_professor"),
    path('student/<int:pk>/', views.view_student, name="view_student"),
    path('school-profit/', views.view_school_profit, name="view_school_profit"),
    path('create-student/', views.create_student, name="create_student"),
    path('update-student/<int:pk>/', views.update_student, name="update_student"),
    path('delete-student/<int:pk>/', views.delete_student, name="delete_student"),
    path('create-professor/', views.create_professor, name="create_professor"),
    path('export-students-excel/', views.export_students_excel, name="export_students_excel"),
]