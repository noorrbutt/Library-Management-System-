from django.contrib import admin
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from django.urls import path, include as url_include
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', url_include('librarymanagement.library.urls')),
    
    # Authentication
    path('adminlogin/', LoginView.as_view(template_name='library/adminlogin.html', next_page='dashboard'), name='adminlogin'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
