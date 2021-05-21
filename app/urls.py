from django.urls import path
from . import views
from .views import RoomListView, BookingList, RoomDetailView, CancelBookingView

urlpatterns = [
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
    path('menu/', views.menu, name="menu"),
    path('about/', views.about, name="about"),
    path('view_section/', views.view_section, name="view_section"),
    path('Manage_Sections/', views.Manage_Sections, name="Manage_Sections"),
    path('Manage_labs_page/', views.Manage_labs_page, name="Manage_labs_page"),
    path('Manage_resources_page/', views.Manage_resources_page, name="Manage_resources_page"),
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
    path('room_list/', views.RoomListView, name = 'RoomListView'),
    path('booking_list/',BookingList.as_view(), name = 'BookingList'),
    path('room/<category>',RoomDetailView.as_view(),name='RoomDetailView'),
    path('booking_cancel/<pk>',CancelBookingView.as_view(), name='CancelBookingView'),
    path("resourcepage/",views.resourcepage,name="resourcepage"),
    path("resource_book/",views.resource_book,name="resource_book"),
    path('delete_resource/<int:pk>/', views.delete_resource, name="delete_resource"),
    path('sendemail/<pk>/',views.sendemail,name="sendemail"),
    path('foremail/',views.foremail,name="foremail"),
    path('delete_booked_lab/<pk>/',views.delete_booked_lab,name="delete_booked_lab"),
]
