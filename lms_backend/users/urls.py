from django.urls import path
from .import views

urlpatterns=[
    path('',views.home_view,name='home'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.login_view,name='logout'),
    path('signup/',views.signup_view,name='signup'),
    path('dashboard/',views.dashboard_view,name='dashboard'),

]