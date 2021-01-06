from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from .views import Student, Lecturer
from .import views

app_name = "users"

urlpatterns = [

    path('', views.home, name='student-home'),
    path('index/', views.index, name='index'),
    path('signup/', views.signup, name='signup_form'),
    #path('<pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('profile/', views.profile, name='profile'),
    path('mystudents/', views.mystudents, name='mystudents'),
    path('my-projects/<str:registration_no>/edit', views.ProjectUpdateView.as_view(), name="project_update"),
    path('project-list/', views.project_list, name='project_list'),
    path('upload/', views.upload_project, name='upload_project'),
    path('upload-project', views.ProjectCreateView.as_view(), name="upload_new_project"),
    path('student_signup/', views.StudentSignUpView.as_view(), name='student_signup'),
    path('lecturer_signup/', views.LecturerSignUpView.as_view(), name='lecturer_signup'),
    path('student_remarks/', views.student_remarks, name='student_remarks'),
    path('add_remarks/', views.add_remarks, name='add_remarks'),
    #path('submit_project/', views.submit_project, name='submit_project'),
    path('upload/', views.upload, name='upload')
 ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
