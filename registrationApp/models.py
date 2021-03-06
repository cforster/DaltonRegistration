from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class House (models.Model):
	houseAdvisorOne_firstName = models.CharField(max_length=128)
	houseAdvisorOne_lastName = models.CharField(max_length=128)
	houseAdvisorTwo_firstName = models.CharField(max_length=128)
	houseAdvisorTwo_lastName = models.CharField(max_length=128)
	roomNumber = models.IntegerField()
	studentNumber = models.IntegerField()

        def __unicode__(self):
	        return self.houseAdvisorOne_firstName

class Parent (models.Model):
	parentFirstName= models.CharField(max_length=128)
	parentLastName= models.CharField(max_length=128)
	parentEmail = models.CharField(max_length=256) 
	parentPhoneNumber = models.IntegerField()
        def __unicode__(self):
	        return self.parentFirstName
	
class ParentStudent (models.Model):
	parentOneID = models.ForeignKey(Parent, related_name =' parent_one')
	parentTwoID = models.ForeignKey(Parent, related_name =' parent_two')
    
        def __unicode__(self):
	        return u'%s' % (self.id)

class Student (models.Model):
	user = models.OneToOneField(User)
	firstName = models.CharField(max_length=128)
	lastName= models.CharField(max_length=128)
	email = models.EmailField()
	grade= models.IntegerField()
	houseID= models.ForeignKey(House)
	parentStudentID= models.ForeignKey(ParentStudent)
	submit = models.BooleanField()
	advisorApproval = models.BooleanField()
	advisor1Note = models.CharField(max_length=100000)
	advisor2Note = models.CharField(max_length=100000)
	advisor1NoteRead = models.BooleanField()
	advisor2NoteRead = models.BooleanField()

	parentApproval = models.BooleanField()
	parentNote = models.CharField(max_length=100000)
	parentNoteRead = models.BooleanField()
	
	activation_key = models.CharField(max_length=40)

        def __unicode__(self):
	        return u'%s %s' %(self.firstName, self.lastName)

class DepartmentChair (models.Model):
	email= models.EmailField()
	firstName = models.CharField(max_length=128)
	lastName = models.CharField(max_length=128)	
        def __unicode__(self):
	        return u'%s %s' %(self.firstName, self.lastName)
# three column table
#grade/course/disc.
#
#

class Discipline (models.Model):
	discipline_Choices= (
		('Math', 'Mathematics'),
		('Science', 'Science'),
		('English', 'English'),
		('History', 'History'),
		('Language', 'Language'),
		('P.E.', 'Physical Education'),
		('Art', 'Art'),
		('Dance','Dance'),
		('Computer Science','Computer Science'),
	)
	discipline = models.CharField(max_length=16, choices= discipline_Choices)
	departmentChair = models.ForeignKey(DepartmentChair)
        def __unicode__(self):
	        return self.discipline

class Course (models.Model):
	courseName = models.CharField(max_length=256)
	courseDescription = models.CharField(max_length=2048)
	preapprovalRequired = models.BooleanField()
	discipline = models.ForeignKey(Discipline)
	grades_Offered = models.CommaSeparatedIntegerField(max_length=16)
	courseNumber = models.IntegerField(max_length=9)

        def __unicode__(self):
	        return self.courseName
#prerequisite
class Section (models.Model):
	courseID = models.ForeignKey(Course)
	semesterOne = models.BooleanField()
	semesterTwo = models.BooleanField()
	roomNumber = models.IntegerField()
	APeriodDays = models.CommaSeparatedIntegerField(max_length=15) 
	BPeriodDays = models.CommaSeparatedIntegerField(max_length=15)
	CPeriodDays = models.CommaSeparatedIntegerField(max_length=15)
	DPeriodDays = models.CommaSeparatedIntegerField(max_length=15)
	EPeriodDays = models.CommaSeparatedIntegerField(max_length=15)
	FPeriodDays = models.CommaSeparatedIntegerField(max_length=15)
	GPeriodDays = models.CommaSeparatedIntegerField(max_length=15)
	HPeriodDays = models.CommaSeparatedIntegerField(max_length=15)
	IPeriodDays = models.CommaSeparatedIntegerField(max_length=15)
	KPeriodDays = models.CommaSeparatedIntegerField(max_length=15)
	ZPeriodDays = models.CommaSeparatedIntegerField(max_length=15)
        def __unicode__(self):
	        return u'%s' % (self.id)

#default value
#scratch column bool

class StudentSchedule (models.Model):
	studentID= models.ForeignKey(Student)
	sectionID= models.ForeignKey(Section)
	rank = models.IntegerField()
        def __unicode__(self):
	        return u'%s' % (self.id)
	        	
class PreApproval (models.Model):
	studentID = models.ForeignKey(Student)
	courseID = models.ForeignKey(Course)
        def __unicode__(self):
	        return u'%s' % (self.id)

