
from django.urls import path
from .import views

urlpatterns = [
   path('categories/',views.category_list_create,name='category_list_create'),
   path('courses/',views.course_list_create,name='courses_list_creatre'),
   path('courses/<int:pk>/',views.course_detail,name='course_detail'),
   path('lesson/',views.lesson_list_create,name='lesson_list_create'),
   path('materials/',views.material_list_create,name='material_list_create'),
   path('enrollments/',views.enrollment_list_create,name='enrollment_list_create'),
   path('questions/',views.questionanswer_list_create,name='questionanswer_list_create'),
    
]
