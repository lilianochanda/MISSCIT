"""MISSCIT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from students.views import home, signup, profile, upload, project_list,  ProjectCreateView, upload_project, ProjectUpdateView, StudentSignUpView, LecturerSignUpView, index, student_remarks, add_remarks

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('students.urls', namespace='users')),

    path('', home, name='student-home'),
    path('index/', index, name='index'),
    #path('<pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('signup/', signup, name='signup_form'),
    path('profile/', profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='students/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='students/logout.html'), name='logout'),
    path('project-list/', project_list, name='project_list'),
    #path('upload/', upload, name='upload'),
    path('upload/', ProjectCreateView.as_view(), name='upload_project'),
    #path('upload-project', ProjectCreateView.as_view(), name="upload_new_project"),
    path('student_signup/', StudentSignUpView.as_view(), name='student_signup'),
    path('lecturer_signup/', LecturerSignUpView.as_view(), name='lecturer_signup'),
    path('student_remarks/', student_remarks, name='student_remarks'),
    path('add_remarks/', add_remarks, name='add_remarks'),
    #path('submit_project/', submit_project, name='submit_project'),
    #path('my-projects/<str:registration_no>/edit', ProjectUpdateView.as_view(), name="project_update"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


