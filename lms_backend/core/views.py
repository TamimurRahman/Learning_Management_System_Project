from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Course,Category,Lesson,Material,Enrollment,QuestionAnswer
from .serializers import CategorySerializer, CourseSerializer,LessonSerializer,MaterialSerializer,QuestionAnswerSerializer,EnrollmentSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def category_list_create(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories,many=True) #jehetu onk gulo category thake
        return Response(serializer.data)
    elif request.method == 'POST':
        if request.user.role !='admin':
            return Response({'detail': 'only admin can create categories'},status=status.HTTP_403_FORBIDDEN)
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() #এইটা Model এর নতুন object ডাটাবেজে তৈরি করে।
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return  Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
'''
1️⃣ Validate করা

is_valid() চালালে serializer চেক করে:

field গুলো ঠিক আছে কিনা,

required field আছে কিনা,

field type সঠিক কিনা,

unique কিনা।

serializer.is_valid()
'''

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def course_list_create(request):
    if request.method == 'GET':
        if request.user.role in ['admin','student']:
            courses = Course.objects.all()
        elif request.user.role == 'teacher':
            courses = Course.objects.filter(teacher=request.user)
        else:
            return Response({'detail':'Unauthorized role'},status=status.HTTP_403_FORBIDDEN)
        
        serializer = CourseSerializer(courses,many=True) #jehetu onk gulo course  thake tahole many true thake
        return  Response(serializer.data)
        
    elif request.method == 'POST':
        if request.user.role !='teacher':
            return Response({'detail': 'only teacher can create categories'},status=status.HTTP_403_FORBIDDEN)
        serializer = CourseSerializer(data=request.data)#নতুন course তৈরি হলে teacher হিসেবে current logged-in user save হবে
        if serializer.is_valid():
            serializer.save(teacher=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return  Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def course_detail(request,pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({'detail':'Course not found'},status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        if request.user.role == 'admin' or request.user == course.instructor_id:
            serializer = CourseSerializer(course)
            return Response(serializer.data)
        return Response({'detail':'Permission denined!!!'},status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'PUT':
        if request.user.role != 'teacher' or request.user != course.instructor_id:
            return Response({'detail':'only course teacher can update this course'},status=status.HTTP_403_FORBIDDEN)
        serializer = CourseSerializer(course,data=request.data)
        if serializer.is_valid():
            serializer.save(instructor_id=request.user)
            return Response(serializer.data)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if request.user.role != 'teacher' or request.user != course.instructor_id:
            return Response({'detail':'only course teacher can delete this course'},status=status.HTTP_403_FORBIDDEN)
        course.delete()
        return Response({'detail':'course deleted'},status = status.HTTP_204_NO_CONTENT)    
        
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def lesson_list_create(request):
    if request.method == 'GET':
        categories = Lesson.objects.all()
        serializer = LessonSerializer(categories,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return  Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def material_list_create(request):
    if request.method == 'GET':
        categories = Material.objects.all()
        serializer = MaterialSerializer(categories,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return  Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def enrollment_list_create(request):
    if request.method == 'GET':
        categories = Enrollment.objects.all()
        serializer = EnrollmentSerializer(categories,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return  Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def questionanswer_list_create(request):
    if request.method == 'GET':
        categories = QuestionAnswer.objects.all()
        serializer = QuestionAnswerSerializer(categories,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = QuestionAnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return  Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)