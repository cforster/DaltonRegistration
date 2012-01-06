from django.contrib import admin

from registrationApp.models import Student
admin.site.register(Student)

from registrationApp.models import House
admin.site.register(House)

from registrationApp.models import Parent
admin.site.register(Parent)

from registrationApp.models import ParentStudent 
admin.site.register(ParentStudent)

from registrationApp.models import DepartmentChair
admin.site.register(DepartmentChair)

from registrationApp.models import Discipline 
admin.site.register(Discipline)

from registrationApp.models import Course
admin.site.register(Course)

from registrationApp.models import Section 
admin.site.register(Section)

from registrationApp.models import StudentSchedule
admin.site.register(StudentSchedule)

from registrationApp.models import PreApproval 
admin.site.register(PreApproval)