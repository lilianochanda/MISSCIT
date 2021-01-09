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
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView
from students.forms import StudentSignUpForm, LecturerSignUpForm
from .decorators import allowed_users
from django.utils import timezone
from django.views import generic
from django.urls import reverse_lazy
from students import models

class ProjectUpdateView(UpdateView):
    model = Project
    template_name = 'project-update.html'
    fields = ('status',)

    def get_context_data(self, **kwargs):
        registration_no = kwargs.get('registration_no')
        context = super().get_context_data(**kwargs)
        context["project"] = get_object_or_404(Project, registration_no=registration_no)
        return context

    def get_success_url(self) -> str:
        return reverse_lazy("mystudents")


def student_remarks(request):
    student = request.user
    projects = student.student_project.all()
    # for project in projects:
    #     # print(dir(project))
    #     print(project.student_projects.all())
    context = {
        'my_projects': projects
    }

    return render(request, 'students/student_remarks.html', context)


def project_list(request):
    projects = Project.objects.all()
    context = {
        'Projects': projects
    }
    return render(request, 'students/project_list.html', context)


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
        return render(request, 'students/upload.html', context)

class ProjectUploadView(CreateView):
    model = Project
    fields = ('phase', 'project_title','registration_no', 'project_brief', 'submission_date', 'supervisor', 'pdf')
    template_name = 'students/upload_project.html'

    def form_valid(self,form):
        user = self.request.user
        project = form.save(commit=False)
        #project.registration_no = user.registration_no
        project.save()
        project.student.add(user)
        project.save()
        print(project.student)
        return super(ProjectUploadView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("users:student_remarks")


def upload_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            project = form.save(commit=False)
            project.student.add(user)
            project.save()
            print(project)
            print(project.student)
        return redirect('project_list')
    else:
        form = ProjectForm()
        projects = Project.objects.all()
    return render(request, 'students/upload_project.html', {'Projects':projects,
        'form': form
    })


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'students/upload_project.html'

    def get_success_url(self):
        return reverse_lazy('projects')

#def submit_project(request, id=None):
    #student = request.user.Student
    #project = get_object_or_404(Project, id=id)
    #lecturer = project.lecturer
    #if request.method == 'POST':
        #form = SubmitForm(request.POST, request.FILES)
        #if form.is_valid():
            #upload = form.save(commit=False)
            #upload.Lecturer = lecturer
            #upload.Student = student
            #upload.submitted_project = Project
            #upload.save()
            #return redirect('student_remarks')
        #else:
            #form = SubmitForm()
            #return render(request, 'students/upload_project.html', {'form': form})


def submit_list(request):
    lecturer = request.user.Lecturer
    return render(request, 'students/mystudents.html', {'lecturer':lecturer})

def home(request):
    if request.user.is_authenticated:
        if request.user.is_lecturer:
            return redirect('users:my_students')
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
    projects = request.user.projects_assigned.all()
    context = {
        'lecturer': lecturer,
        'my_projects': request.user.projects_assigned.all()
    }
    return render(request, 'students/mystudents.html', context)

def all_projects(request):
    if request.user.is_superuser:
        projects = Project.objects.all()
        context = {
            'Projects': projects
        }
        return render(request, 'students/complete_projects.html', context)
    else:
        return render(request, 'students/home.html')

@login_required
def profile(request):
    print(dir(request.user))
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


def add_remarks(request):
    remarks_obtained = False
    #student = get_object_or_404(models.Student)
    if request.method == "POST":
        form = RemarksForm(request.POST)
        if form.is_valid():
            remarks = form.save(commit=False)
            # remarks.student = Student
            remarks.student =form.cleaned_data.get('student')
            remarks.lecturer = request.user.lecturer
            remarks.save()
            messages.success(request, 'remarks uploaded successfully!')
            return redirect('students/my_students')
    else:
        form = RemarksForm()
    return render(request, 'students/add_remarks.html', {'form':form, 'remarks_obtained':remarks_obtained})


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

