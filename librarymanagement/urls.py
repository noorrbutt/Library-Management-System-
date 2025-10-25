from django.contrib import admin
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from django.urls import path
from librarymanagement.library import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    # Home & login
    path('', views.home_view, name='home'),
    path('adminclick/', views.adminclick_view, name='adminclick'),
    path('adminsignup/', views.adminsignup_view, name='adminsignup'),
    path('adminlogin/', LoginView.as_view(template_name='library/adminlogin.html'), name='adminlogin'),

    # logout line
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('afterlogin/', views.afterlogin_view, name='afterlogin'),

    # Admin: Book management
    path('addbook/', views.addbook_view, name='addbook'),
    path('viewbook/', views.viewbook_view, name='viewbook'),
    path('issuebook/', views.issuebook_view, name='issuebook'),
    path('viewissuedbook/', views.viewissuedbook_view, name='viewissuedbook'),
    path('deletebooks/', views.delete_books_view, name='deletebooks'),
    path('updatebooks/', views.update_books_view, name='updatebooks'),
    path('return-issued-book/', views.return_issued_book_view, name='return_issued_book'),
    path('update-issued-books/', views.update_issued_books_view, name='update_issued_books'),

    # Admin: Student management
    path('addstudent/', views.addstudent_view, name='addstudent'),
    path('studentadded/', views.studentadded_view, name='studentadded'),
    path('viewstudent/', views.viewstudent_view, name='viewstudent'),
    path('deletestudents/', views.delete_students_view, name='deletestudents'),
    path('updatestudents/', views.update_students_view, name='updatestudents'),


]
