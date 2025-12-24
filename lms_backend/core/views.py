from django.shortcuts import render,redirect
from django.db.models import Q, Count
from .import models
from django.core.paginator import Paginator
def courses_list_view(request):
    courses = models.Course.objects.filter(is_active=True).select_related('instructor_id','category_id')
    categories = models.Category.objects.filter(is_active=True)
    search = request.GET.get('search')

    if search:
        courses = courses.filter(
            Q(title__icontains=search)|
            Q(description__icontains=search)|
            Q(instructor_id__first_name__icontains=search)|
            Q(instructor_id__last_name__icontains=search)
        )
    
    #Category Filter
    category_filter = request.GET.get('category')
    if category_filter:
        courses = courses.filter(category_id__id=category_filter)
    
    #Price Filter
    price_filter = request.GET.get('price')
    if price_filter == 'free':
        courses = courses.filter(price=0)
    elif price_filter == 'paid':
        courses = courses.filter(price__gt=0)

    #sort functionality
    sort_by = request.GET.get('sort','popular')
    if sort_by == 'newest':
        courses = courses.order_by('-created_at')# descending order
    elif sort_by == 'price_low':
        courses = courses.order_by('price') # ascending order
    elif sort_by == 'price_high':
        courses = courses.order_by('-price') # desending order
    else:
        courses = courses.annotate(enrollment_count = Count('enrollment')).order_by('-enrollment_count')

    #Paginator
    paginator = Paginator(courses,12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context ={
        'courses':page_obj,
        'categories':categories,
        'search':search,
        'category_filter':category_filter,
        'price_filter':price_filter,
        'sort_by':sort_by,
    }

    return render(request,'',context)