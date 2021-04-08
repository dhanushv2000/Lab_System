from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from django.core.mail import send_mail
from Lab_System.settings import *
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
# Create your views here.
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .filters import studentfilter

from .models import *
from django.views.generic import ListView, FormView, View, DeleteView
from app.availability import *
from django.urls import reverse, reverse_lazy

def home(request):
    return render(request,'app/home.html')


def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')


		context = {'form':form}
		return render(request, 'app/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		context = {}
		return render(request, 'app/DashBoard.html', context)
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				context = {}
				return render(request, 'app/DashBoard.html', context)
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'app/login.html', context)

def logoutUser(request):
	logout(request)
	return render(request,'app/home.html')

def DashBoard(request):
    sec = Section.objects.filter(faculty__username = request.user.username)
    return render(request, 'app/DashBoard.html',{'sec':sec})

def students(request):
    stud = Student_link.objects.filter(section__faculty__username = request.user.username)
    myFilter = studentfilter(request.GET, queryset = stud)
    stud = myFilter.qs

    return render(request, 'app/students.html',{'stud':stud,'myFilter':myFilter})

def student_id(request, pk):
    student = Student_link.objects.get(id=pk)
    return render(request, 'app/student_id.html',{'student':student})

def create_section(request):
    form = CreateSection()
    user_email=request.user.email
    print(user_email, "!!!!")
    if request.method == 'POST':
        #print('Printing: ',request.POST)
        form = CreateSection(request.POST)
        print("Before validation")
        if form.is_valid():
            print("form is valid !!!")
            post = form.save(commit = False)
            post.faculty = request.user
            #data= post.cleaned_data
            html_content = render_to_string('createsectionemail.html',{'post':post})
            text_content = strip_tags(html_content)
            msg=EmailMultiAlternatives(
            #subject
            'You have been added to a section',
            #message
            text_content,
            #from
            EMAIL_HOST_USER,
            #to
            [user_email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            print("Mail successfully sent")

            post.save()
            return redirect('DashBoard')

    context = {'form':form}
    return render(request, 'app/create_section.html',context)

def Create_Student(request):
    form = CreateStudent()

    if request.method == 'POST':
        form = CreateStudent(request.POST)
        if form.is_valid():
            data= form.cleaned_data
            html_content = render_to_string('createstudentemail.html',{'data':data})
            text_content = strip_tags(html_content)
            msg=EmailMultiAlternatives(
            #subject
            'You have been added to a section',
            #message
            text_content,
            #from
            EMAIL_HOST_USER,
            #to
            [data['email']]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            print("Mail successfully sent")

            form.save()
            return redirect('students')

    context = {'form':form}

    return render(request, 'app/Create_student.html', context)

def update_student_id(request,pk):
    student = Student_link.objects.get(id=pk)
    form = CreateStudent(instance=student)

    if request.method == 'POST':
        form = CreateStudent(request.POST, instance=student)
        if form.is_valid():
            data= form.cleaned_data
            form.save()
            html_content = render_to_string('updatestudentemail.html',{'data':data})
            text_content = strip_tags(html_content)
            msg=EmailMultiAlternatives(
            #subject
            'Your information is updated',
            #message
            text_content,
            #from
            EMAIL_HOST_USER,
            #to
            [data['email']]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            print("Mail successfully sent")
            return redirect('students')

    context = {'form':form}
    return render(request, 'app/Create_student.html', context)

def delete_section(request,pk):
    sec = Section.objects.get(id=pk)
    user=request.user.email
    if request.method == "POST":
        html_content = render_to_string('deletesectionemail.html',{'sec':sec})
        sec.delete()
        text_content = strip_tags(html_content)
        msg=EmailMultiAlternatives(
        #subject
        'Section deleted successfully',
        #message
        text_content,
        #from
        EMAIL_HOST_USER,
        #to
        [user]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print("Mail successfully sent")
        return redirect('DashBoard')
    context = {'sec':sec}
    return render(request, 'app/delete_section.html', context)

def delete_student(request,pk):
    sec = Student_link.objects.get(id=pk)
    user=request.user.email
    if request.method == "POST":
        html_content = render_to_string('deletestudentemail.html',{'sec':sec})
        sec.delete()
        text_content = strip_tags(html_content)
        msg=EmailMultiAlternatives(
        #subject
        'You have been removed from a section',
        #message
        text_content,
        #from
        EMAIL_HOST_USER,
        #to
        [sec.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print("Mail successfully sent")
        return redirect('students')
    context = {'sec':sec}
    return render(request, 'app/delete_student.html', context)

def RoomListView(request):
    room = Room.objects.all()[0]
    room_categories = dict(room.ROOM_CATEGORIES)
    room_list = []
    for room_category in room_categories:
        room = room_categories.get(room_category)
        room_url = reverse('RoomDetailView', kwargs={'category':room_category})
        room_list.append((room,room_url))
    context= {"room_list":room_list}
    return render(request, 'room_list_view.html', context)



class BookingList(ListView):
    model = Booking
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list


class RoomDetailView(View):
    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category',None)
        form = AvailabilityForm()
        section = Section.objects.filter(faculty = self.request.user)
        room_list = Room.objects.filter(category = category)

        if (len(room_list)>0):
            room = room_list[0]
            room_category = dict(room.ROOM_CATEGORIES).get(room.category,None)
            context = {'room_category':room_category, 'form':form, 'section': section}
            return render(request, 'room_detail_view.html', context)
        else:
            return HttpResponse('category does not exist or you have no sections to book')


    def post(self,request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        room_list = Room.objects.filter(category = category)
        section_list = Section.objects.filter(faculty=self.request.user)
        form = AvailabilityForm(request.POST)
        data_check_in = ""
        data_check_out = ""
        post = form
        if form.is_valid():
            post = form.save(commit=False)
        available_rooms = []


        for room in room_list:
            if check_availability(room,post.check_in,post.check_out):
                available_rooms.append(room)

        if len(available_rooms)>0:
            room = available_rooms[0]

            post.user = self.request.user
            post.room = room
            if form.is_valid():
                post.save()
            context= {'booking':post}
            return render(request,'booking_success.html',context)
        else:
            return HttpResponse("All of this category of rooms are booked!! Try another one")


class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_cancel_view.html'
    success_url = reverse_lazy('BookingList')

def resource_book(request):
    user=request.user.email
    form = book()
    if request.method=="POST":
        form=book(request.POST)
        if form.is_valid():
            data= form.cleaned_data
            html_content = render_to_string('bookresourceemail.html',{'data':data})
            text_content = strip_tags(html_content)
            msg=EmailMultiAlternatives(
            #subject
            'Resource selected successfully',
            #message
            text_content,
            #from
            EMAIL_HOST_USER,
            #to
            [user]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            print("Mail successfully sent")

            form.save()
            return redirect("resource_book")
    return  render(request,'resource_book.html',{'form':form})

def resourcepage(request):
    res=resource_booking.objects.filter(select_booking__user__username = request.user.username)
    return render(request,'resource.html',{'res':res})

def delete_resource(request,pk):
    sec = resource_booking.objects.get(id=pk)
    user=request.user.email
    if request.method == "POST":
        html_content = render_to_string('deleteresourceemail.html',{'sec':sec})
        sec.delete()
        text_content = strip_tags(html_content)
        msg=EmailMultiAlternatives(
        #subject
        'Resource unselected',
        #message
        text_content,
        #from
        EMAIL_HOST_USER,
        #to
        [user]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print("Mail successfully sent")
        return redirect('resourcepage')
    context = {'sec':sec}
    return render(request, 'app/delete_resource.html', context)

def delete_booked_lab(request,pk):
    sec = Booking.objects.get(id=pk)
    user=request.user.email
    if request.method == "POST":
        html_content = render_to_string('deletelabemail.html',{'sec':sec})
        sec.delete()
        text_content = strip_tags(html_content)
        msg=EmailMultiAlternatives(
        #subject
        'Lab deleted successfully',
        #message
        text_content,
        #from
        EMAIL_HOST_USER,
        #to
        [user]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print("Mail successfully sent")
        return redirect('DashBoard')
    context = {'sec':sec}
    return render(request, 'booking_cancel_view.html', context)

def sendemail(request,pk):
    booking=Booking.objects.get(id=pk)
    user=request.user.email
    print('user:   ',user)
    students=Student_link.objects.filter(section__faculty=request.user).values_list('email',flat=True)
    emails=[]
    for email in students:
        emails.append(email)
    print("==================",emails)
    emails.append(user)
    html_content = render_to_string('foremail.html', {'booking':booking})
    text_content = strip_tags(html_content)
    msg=EmailMultiAlternatives(
    #subject
    'Booking of lab',
    #message
    text_content,
    #from
    EMAIL_HOST_USER,
    #to
    emails
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print("Mail successfully sent")
    return redirect('DashBoard')

def foremail(request):
    booking=Booking.objects.all()
    return render(request,'foremail.html',{'booking':booking})
