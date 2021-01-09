from django.contrib import admin
from students.models import Profile, Student, Lecturer, User, Project, Category, LecturerRemarks, StudentRemarks
from . import models
admin.site.register(Profile)
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Lecturer)
admin.site.register(Project)
admin.site.register(Category)
admin.site.register(LecturerRemarks)
admin.site.register(StudentRemarks)


#@admin.register(models.Project)
#class StudentAdmin(admin.ModelAdmin):
    #prepopulated_fields = {'title': ('title',)}