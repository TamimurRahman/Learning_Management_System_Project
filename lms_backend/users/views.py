from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import User
from . import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib import messages
from core import models
from django.views.decorators.csrf import csrf_protect
# Create your views here.



User = get_user_model()
def signup_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return redirect('dashboard')
        return render(request,'')
    
    elif request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        username=request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        role = request.POST.get('role')

        if password != password_confirm:
            messages.error(request,'Password do not match!')
            return render(request,'')
        if User.objects.filter(username=username).exists():
            messages.error(request,'Username already exists!')
            return render(request,'')
        if User.objects.filter(email=email).exists():
            messages.error(request,'Email already exists!')
            return render(request,'')
        user = User.objects.create_user(

            username = username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role
        )
        login(request,user)
        return redirect('dashboard')
        

@csrf_protect
def login_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return redirect('dashboard')
        return render(request,'')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid username or password')
            return render(request,'')



def dashboard_view(request):
    user = request.user
    context = {'user':user}

    if user.role == 'teacher':
        teacher_courses = models.Course.objects.filter(instructor_id = user)
        total_students = models.Enrollment.objects.filter(course_id__instructor_id=user).count()
        context.update({
            'courses':teacher_courses,
            'total_courses':teacher_courses.count(),
            'total_students':total_students,
            'total_hours':sum([course.duration for course in teacher_courses])
        })
        return render(request,'',context)
    else:
        enrollments = models.Enrollment.objects.filter(student_id = user)
        completed_course = enrollments.filter(is_completed=True).count()
        context.update({
            'enrollments':enrollments,
            'total_enrolled':enrollments.count(),
            'completed_course':completed_course,
            'certificate_earned':enrollments.filter(is_certificate_ready=True).count(),
            'total_hours':sum([e.course_id.duration for e in enrollments if e.is_completed ])
        })

        return render(request,'',context)









@api_view(['GET','POST'])
def user_list_create(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return Response({'detail':'Authentication credentials where not provided'},status=status.HTTP_401_UNAUTHORIZED)
        
        if request.user.role == 'admin':
            users = User.objects.all()
        else:
            users = User.objects.filter(id=request.user.id)
        serializer = serializers.UserSerializer(users, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

