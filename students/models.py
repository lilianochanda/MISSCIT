from django.db import models
from django.contrib.auth.models import AbstractUser, User
from PIL import Image
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    createdon = models.DateTimeField(auto_now_add=True)
    updatedon = models.DateTimeField(auto_now=True)


class Lecturer(models.Model):
    user = models.OneToOneField(User, related_name="lecturer", on_delete=models.CASCADE, null=True)
    staff_no = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(User, related_name="student", on_delete=models.CASCADE, null=True)
    registration_no = models.CharField(max_length=100)
    course = models.CharField(max_length=50)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username


class Project(models.Model):
    PHASE_CHOICES = [
        ('PROJECT_CONCEPT', 'project concept'),
        ('FIRST_CHAPTERS', 'first chapters'),
        ('DRAFT_PROJECT', 'draft project'),
        ('FINAL_PROJECT', 'final project'),
    ]
    phase = models.CharField(max_length=30, choices=PHASE_CHOICES, default='PROJECT_CONCEPT')
    student = models.ForeignKey(Student, related_name='student_project', on_delete=models.CASCADE)
    project_title = models.CharField(max_length=100)
    registration_no = models.CharField(max_length=100, primary_key=True)
    project_brief = models.TextField(default='description')
    submission_date = models.DateTimeField()
    pdf = models.FileField(upload_to='projects/pdf/')

    def __str__(self):
        return self.project_title





class LecturerRemarks(models.Model):
    PHASE_CHOICES = [
        ('PROJECT_CONCEPT', 'project concept'),
        ('FIRST_CHAPTERS', 'first chapters'),
        ('DRAFT_PROJECT', 'draft project'),
        ('FINAL_PROJECT', 'final project'),
    ]
    phase = models.CharField(max_length=30, choices=PHASE_CHOICES, default='PROJECT_CONCEPT')
    project_title = models.ForeignKey(Project, related_name='student_projects', on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, related_name='student_obtained_remarks', on_delete=models.CASCADE, null=True)
    lecturer = models.ForeignKey(Lecturer, related_name='lecturer_give_remarks', on_delete=models.CASCADE, null=True)
    remarks_obtained = models.TextField()
    STATUS_CHOICES = [
        ('APPROVED', 'APPROVED'),
        ('REJECTED', 'REJECTED'),
        ('APPROVED WITH REMARKS', 'APPROVED WITH REMARKS'),
    ]
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)

    def __str__(self):
        return self.project_title


class SubmitProject(models.Model):
    student = models.ForeignKey(Student, related_name='student_submit', on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Lecturer, related_name='lecturer_submit',on_delete=models.CASCADE)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    #pdf = models.Foreignkey(Project, related_name='submission_for_project', on_delete=models.CASCADE)
    submit = models.FileField(upload_to='submission')

    def __str__(self):
        return "submitted+str(self.submitted_project.project_title)"

    class Meta:
        ordering = ['uploaded_on']


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'categories'
    name = models.CharField(max_length=40)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)




