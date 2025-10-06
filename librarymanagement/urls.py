from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from librarymanagement.library import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('librarymanagement.library.urls')),


    path('', views.home_view, name='home'),

    path('adminclick/', views.adminclick_view, name='adminclick'),
    path('studentclick/', views.studentclick_view, name='studentclick'),

    path('adminsignup/', views.adminsignup_view, name='adminsignup'),
    path('studentsignup/', views.studentsignup_view, name='studentsignup'),

    path('adminlogin/', LoginView.as_view(template_name='library/adminlogin.html'), name='adminlogin'),
    path('studentlogin/', LoginView.as_view(template_name='library/studentlogin.html'), name='studentlogin'),

    path('logout/', LogoutView.as_view(template_name='library/index.html'), name='logout'),
    path('afterlogin/', views.afterlogin_view, name='afterlogin'),

    # Admin actions
    path('addbook/', views.addbook_view, name='addbook'),
    path('viewbook/', views.viewbook_view, name='viewbook'),
    path('issuebook/', views.issuebook_view, name='issuebook'),
    path('viewissuedbook/', views.viewissuedbook_view, name='viewissuedbook'),
    path('viewstudent/', views.viewstudent_view, name='viewstudent'),

    # Student actions
    path('viewissuedbookbystudent/', views.viewissuedbookbystudent, name='viewissuedbookbystudent'),

    # Info pages
    path('aboutus/', views.aboutus_view, name='aboutus'),
    path('contactus/', views.contactus_view, name='contactus'),
]
