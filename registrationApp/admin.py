from django.contrib import admin

from registrationApp.models import Student
admin.site.register(Student)

from registrationApp.models import House
admin.site.register(House)

from registrationApp.models import Parent
admin.site.register(Parent)

from registrationApp.models import ParentStudent 
admin.site.register(ParentStudent)

from registrationApp.models import StudentHouseParent
admin.site.register(StudentHouseParent)

from registrationApp.models import Discipline 
admin.site.register(Discipline)

from registrationApp.models import Course
class CourseAdmin(admin.ModelAdmin):
    search_fields = ['courseName']

admin.site.register(Course, CourseAdmin)

from registrationApp.models import Section 
admin.site.register(Section)

from registrationApp.models import StudentSchedule
class StudentScheduleAdmin(admin.ModelAdmin):
    search_fields = ['studentID.first_name','studentID.last_name']

admin.site.register(StudentSchedule, StudentScheduleAdmin)

from registrationApp.models import PreApproval 
admin.site.register(PreApproval)

from registrationApp.models import CourseDiscipline
admin.site.register(CourseDiscipline)

from registrationApp.models import RequiredObjects
admin.site.register(RequiredObjects)

from registrationApp.models import AlternateCourse
admin.site.register(AlternateCourse)