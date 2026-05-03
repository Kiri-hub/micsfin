from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('', views.homepage, name="homepage"),
    path('view-student/<int:pk>/', views.view_student, name="view_student"),
    path('view-school-profit/', views.view_school_profit, name="view_school_profit"),
    path('view-professors/', views.view_professors, name="view_professors"),
    path('view-professor/<int:pk>/', views.view_professor, name="view_professor"),
]