from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *

# Create your views here.

from .models import *
from .forms import CreateUserForm

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
    sec = Section.objects.all()
    return render(request, 'app/DashBoard.html',{'sec':sec})

def students(request):
    stud = Student_link.objects.all()
    return render(request, 'app/students.html',{'stud':stud})

def student_id(request, pk):
    student = Student_link.objects.get(id=pk)
    return render(request, 'app/student_id.html',{'student':student})

def create_section(request):
    form = CreateSection()

    if request.method == 'POST':
        #print('Printing: ',request.POST)
        form = CreateSection(request.POST)
        if form.is_valid():
            form.save()
            return redirect('DashBoard')

    context = {'form':form}
    return render(request, 'app/create_section.html',context)

def Create_Student(request):
    form = CreateStudent()

    if request.method == 'POST':
        form = CreateStudent(request.POST)
        if form.is_valid():
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
            form.save()
            return redirect('students')

    context = {'form':form}
    return render(request, 'app/Create_student.html', context)

def delete_section(request,pk):
    sec = Section.objects.get(id=pk)

    if request.method == "POST":
        sec.delete()
        return redirect('DashBoard')
    context = {'sec':sec}
    return render(request, 'app/delete_section.html', context)

def delete_student(request,pk):
    sec = Student_link.objects.get(id=pk)

    if request.method == "POST":
        sec.delete()
        return redirect('students')
    context = {'sec':sec}
    return render(request, 'app/delete_student.html', context)
