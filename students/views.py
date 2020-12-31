from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# Create your views here.
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# from .forms  import ProjectsForm
# from .models import Projects
from django.contrib.auth import login, authenticate
#from students.forms import SignUpForm
# from .forms  import DocumentForm, UserUpdateForm, ProfileUpdateForm
from students.forms import UserCreationForm,  UserUpdateForm, ProfileUpdateForm, ProjectForm, RemarksForm
from django.contrib import messages
from students.models import Project, Student, Lecturer, User, Category
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, TemplateView, DetailView
from students.forms import StudentSignUpForm, LecturerSignUpForm, SubmitForm
from .decorators import allowed_users
from django.utils import timezone
from django.views import generic


def student_remarks(request):
    projects = Project.objects.all()
    return render(request, 'students/student_remarks.html',{
        'Projects': projects
    })


def project_list(request):
    projects = Project.objects.all()

    return render(request, 'students/project_list.html', {
        'Projects': projects
    })


def upload_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('student_remarks')
    else:
        form = ProjectForm()
    return render(request, 'students/upload_project.html', {
        'form': form
    })


def submit_project(request, id=None):
    student = request.user.Student
    project = get_object_or_404(Project, id=id)
    lecturer = project.lecturer
    if request.method == 'POST':
        form = SubmitForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.Lecturer = lecturer
            upload.Student = student
            upload.submitted_project = Project
            upload.save()
            return redirect('student_remarks')
        else:
            form = SubmitForm()
            return render(request, 'students/upload_project.html', {'form': form})


def submit_list(request):
    lecturer = request.user.Lecturer
    return render(request, 'students/mystudents.html', {'lecturer':lecturer})

def home(request):
    if request.user.is_authenticated:
        if request.user.is_lecturer:
            return redirect('users:mystudents')
        else:
            return render(request, 'students/home.html')
    return render(request, 'students/home.html')


def logout(request):
    return render(request, 'students/logout.html')


def signup(request):
    return render(request, 'students/signup_form.html')


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'students/student_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        return redirect('login')


class LecturerSignUpView(CreateView):
    model = User
    form_class = LecturerSignUpForm
    template_name = 'students/lecturer_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'lecturer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        return redirect('login')

# def topics(request):
    # project = Projects.fields.all()
    # return render(request, 'students/topics.html',{
    # 'project': Projects
# })



def mystudents(request):
    lecturer = request.user.lecturer
    return render(request, 'students/mystudents.html', {'lecturer': lecturer})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'your account has been updated')
        return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'u_form': u_form,
            'p_form': p_form
        }
    return render(request, 'students/profile.html', context)


def index(request):
    Category.objects.all()

    context = {
        'Categories': Category.objects.all()
    }

    return render(request, 'students/main.html', context)


def add_remarks(request,pk):
    remarks_given = False
    student = get_object_or_404(models.Student, pk=pk)
    if request.method == "POST":
        form = RemarksForm(request.POST)
        if form.is_valid():
            remarks = form.save(commit=False)
            remarks.student = student
            remarks.teacher = request.user.Teacher
            remarks.save()
            messages.success(request, 'Marks uploaded successfully!')
            return redirect('students:mystudents')
    else:
        form = RemarksForm()
    return render(request, 'students/add_marks.html', {'form':form, 'student':student, 'remarks_given':remarks_given})


#class IndexView(generic.ListView):
    #template_name = 'students/main.html'

    #def get_queryset(self):
        #context = super().ge
# t_context_data(**kwargs)
        #context['Projects'] = Project.objects.all()
        #return Project.objects.all()


#class ProjectDetailView(DetailView):
    #model = Project
    #template_name = 'students/project_detail.html'

    #def get_context_data(self, **kwargs):
        #context = super().get_context_data(**kwargs)
        #context['Projects'] = Project.objects.all()
        #return context

