from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save
#take out this def

class HouseAdvisor (User):
	favoriteColor = models.CharField(max_length=128,  blank = True, null = True)	
	objects = UserManager()

class House (models.Model):
	houseAdvisorOneID = models.ForeignKey(HouseAdvisor, related_name = 'advisor_one')
	houseAdvisorTwoID = models.ForeignKey(HouseAdvisor, related_name = 'advisor_two', blank = True, null = True)
	roomNumber = models.IntegerField()
        def __unicode__(self):
	        return u'%s %s' % (self.houseAdvisorOneID.first_name,self.houseAdvisorOneID.last_name )

class Parent (models.Model):
	parentFirstName= models.CharField(max_length=128)
	parentLastName= models.CharField(max_length=128)
	parentEmail = models.EmailField(max_length=256)
	parentPhoneNumber = models.IntegerField()
        def __unicode__(self):
	        return self.parentFirstName
	
class ParentStudent (models.Model):
	parentOneID = models.ForeignKey(Parent, related_name =' parent_one')
	parentTwoID = models.ForeignKey(Parent, related_name =' parent_two', blank = True, null = True)
        def __unicode__(self):
	        return u'%s %s' % (self.parentOneID.parentFirstName, self.parentOneID.parentLastName)

class Student (User):
	graduationYear= models.IntegerField()
	houseID= models.ForeignKey(House)
	parentStudentID= models.ForeignKey(ParentStudent)
	submit = models.BooleanField()
	advisorApproval = models.BooleanField()
	advisor1Note = models.CharField(max_length=2000, null=True, blank=True)
	advisor2Note = models.CharField(max_length=2000, null=True, blank=True)
	parentNote = models.CharField(max_length=2000, null=True, blank=True)
	advisor1NoteRead = models.BooleanField()
	advisor2NoteRead = models.BooleanField()
	parentApproval = models.BooleanField()
	parentNoteRead = models.BooleanField()
	activation_key = models.CharField(max_length=40, blank = True, null = True)
	objects = UserManager()
        def __unicode__(self):
	        return u'%s %s' %(self.first_name, self.last_name)

class DepartmentChair (User):
	favoriteColor = models.CharField(max_length=128,  blank = True, null = True)	
	objects = UserManager()
        def __unicode__(self):
	        return u'%s %s' %(self.first_name, self.last_name)

class Discipline (models.Model):
	discipline_Choices= (
		('Math', 'Math'),
		('Science', 'Science'),
		('English', 'English'),
		('History', 'History'),
		('Language', 'Language'),
		('PE', 'PE'),
		('Art', 'Art'),
		('Dance','Dance'),
		('Computer-Science','Computer-Science'),
		('Music','Music'),
		('Misc','Misc')
	)

	discipline = models.CharField(max_length=16, choices= discipline_Choices)
	departmentChair = models.ForeignKey(DepartmentChair)
        def __unicode__(self):
	        return self.discipline

class Course (models.Model):
	courseNumber = models.IntegerField(db_index=True, max_length=9, primary_key=True)
	courseName = models.CharField(max_length=256)
	courseDescription = models.CharField(max_length=2000, blank = True, null = True)
	preapprovalRequired = models.BooleanField()
	alternateRequired = models.BooleanField()
	gradesOffered = models.CommaSeparatedIntegerField(db_index=True, max_length=16)
	prerequisite = models.CharField(max_length = 2000, blank = True, null = True)
	corequisite = models.CharField(max_length = 2000, blank = True, null = True)
	courseCredit = models.CharField(max_length = 200, blank = True, null = True)
	rankChoices = (
		('EngHist', 'EngHist'),
		('English', 'English'),
	)
	rankType = models.CharField(max_length=10, choices = rankChoices, blank = True, null = True)
        def __unicode__(self):
	        return self.courseName

class CourseDiscipline (models.Model):
	courseID = models.ForeignKey(Course)
	discipline = models.ForeignKey(Discipline)
        def __unicode__(self):
	        return u'%s' % (self.id)

class Section (models.Model):
	courseID = models.ForeignKey(Course, db_index=True)
	semesterOne = models.BooleanField()
	semesterTwo = models.BooleanField()
	APeriodDays = models.CommaSeparatedIntegerField(max_length=15, null=True, blank=True) 
	BPeriodDays = models.CommaSeparatedIntegerField(max_length=15, null=True, blank=True)
	CPeriodDays = models.CommaSeparatedIntegerField(max_length=15, null=True, blank=True)
	DPeriodDays = models.CommaSeparatedIntegerField(max_length=15, null=True, blank=True)
	EPeriodDays = models.CommaSeparatedIntegerField(max_length=15, null=True, blank=True)
	FPeriodDays = models.CommaSeparatedIntegerField(max_length=15, null=True, blank=True)
	GPeriodDays = models.CommaSeparatedIntegerField(max_length=15, null=True, blank=True)
	HPeriodDays = models.CommaSeparatedIntegerField(max_length=15, null=True, blank=True)
	IPeriodDays = models.CommaSeparatedIntegerField(max_length=15, null=True, blank=True)
	KPeriodDays = models.CommaSeparatedIntegerField(max_length=15, null=True, blank=True)
	ZPeriodDays = models.CommaSeparatedIntegerField(max_length=15, null=True, blank=True)
	#Instructor
        def __unicode__(self):
	        return u'%s %s' % (self.courseID.courseName, self.id)


class StudentSchedule (models.Model):
	studentID= models.ForeignKey(Student)
	sectionID= models.ForeignKey(Section)
	rank = models.IntegerField(null=True, blank=True)
	alternateFor = models.ForeignKey(Course, null=True, blank=True)
        def __unicode__(self):
	        return u'%s' % (self.id)
	        	
class PreApproval (models.Model):
	studentID = models.ForeignKey(Student)
	courseID = models.ForeignKey(Course)
        def __unicode__(self):
	        return u'%s %s' % (self.studentID.firstName, self.courseID.courseName)

gradeChoices= (
		('9', '9'),
		('10', '10'),
		('11', '11'),
		('12', '12'),
)

class RequiredObjects(models.Model):
	courseID = models.ForeignKey(Course, null=True, blank=True)
	discipline = models.ForeignKey(Discipline, null=True, blank=True)

	grade = models.CharField(max_length=16, choices= gradeChoices)
	message = models.CharField(max_length=2048)
	def __unicode__(self):
		return u'%s %s' % (self.grade, self.courseID)

class AlternateCourse(models.Model):
	courseID = models.ForeignKey(Course)
	grade = models.CharField(max_length=16, choices= gradeChoices)
	def __unicode__(self):
		return u'%s %s' % (self.grade, self.courseID)
#preferences view
#schedule output...

#visuaaolart
#Inter disc