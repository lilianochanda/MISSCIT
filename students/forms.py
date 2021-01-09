from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Project, Student, User, Lecturer, LecturerRemarks
from django.db import transaction
#from django.contrib.auth import get_user_model
#queryset = get_user_model().objects.all()


#class SignUpForm(UserCreationForm):
    # position_choices = forms.CharField(label='ARE YOU A?', widget=forms.RadioSelect(choices=POSITION_CHOICES))
    #username = forms.CharField(max_length=30, required=False)
    #first_name = forms.CharField(max_length=30, required=False)
    #last_name = forms.CharField(max_length=30, required=False)
    #email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')


#class Meta:
    #model = User
    #fields = ['position_choices', 'username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username',  'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['phase', 'project_title', 'project_brief', 'submission_date', 'supervisor', 'pdf']


#class SubmitForm(forms.ModelForm):
    #class Meta:
        #model = SubmitProject
        #fields = ['submit']


class RemarksForm(forms.ModelForm):
    class Meta():
        model = LecturerRemarks
        fields = ['project_title', 'phase', 'status', 'remarks_obtained']


#class StudentRemarksForm(forms.ModelForm):
    #class Meta:
       # model = StudentRemarks
       # fields = ['phase']



class StudentSignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=False)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    registration_no = forms.CharField(max_length=30, required=False)

    class Meta(UserCreationForm.Meta):
        model = User


    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        student = Student.objects.create(user=user)
        student.registration_no = self.cleaned_data.get('registration_no')
        student.save()
        return student


class LecturerSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    staff_number = forms.CharField(max_length=30, required=False)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_lecturer = True
        user.is_staff = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        lecturer = Lecturer.objects.create(user=user)
        #lecturer.staff_no = self.cleaned_data.get('staff_no')
        lecturer.save()
        return lecturer
