from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('DashBoard/', views.DashBoard, name="DashBoard"),
    path('students/', views.students, name="students"),
    path('student_id/<str:pk>/', views.student_id, name="student_id"),
    path('create_section/', views.create_section, name="create_section"),
    path('Create_Student/', views.Create_Student, name="Create_Student"),
    path('update_student_id/<str:pk>/', views.update_student_id, name="update_student_id"),
    path('delete_section/<int:pk>/', views.delete_section, name="delete_section"),
    path('delete_student/<int:pk>/', views.delete_student, name="delete_student"),
    path('', views.home, name="home"),
]
