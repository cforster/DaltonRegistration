from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save

class House (models.Model):
	houseAdvisorOneID = models.ForeignKey(User, related_name = 'advisor_one', limit_choices_to={'groups__in': [3]})
	houseAdvisorTwoID = models.ForeignKey(User, related_name = 'advisor_two', blank = True, null = True,  limit_choices_to={'groups__in': [3]})
	roomNumber = models.IntegerField(blank = True, null = True)
        def __unicode__(self):
	        return u'%s %s House' % (self.houseAdvisorOneID.first_name, self.houseAdvisorOneID.last_name )

class Parent (models.Model):
	parentFirstName= models.CharField(max_length=128)
	parentLastName= models.CharField(max_length=128)
	parentEmail = models.EmailField(max_length=256)
	parentPhoneNumber = models.IntegerField(blank = True, null = True)
        def __unicode__(self):
	        return u'%s %s' % (self.parentFirstName, self.parentLastName)

class ParentStudent (models.Model):
	parentOneID = models.ForeignKey(Parent, related_name =' parent_one')
	parentTwoID = models.ForeignKey(Parent, related_name =' parent_two', blank = True, null = True)
        def __unicode__(self):
	        return u'%s' % (self.parentOneID)

class Student (User):
	graduationYear= models.IntegerField()
	submit = models.BooleanField()
	advisorNote = models.TextField(max_length = 65000,null=True, blank=True)
	parentNote = models.TextField(max_length = 65000,null=True, blank=True)
	studentNote = models.TextField(max_length = 65000,null=True, blank=True)
	advisorNoteRead = models.BooleanField()
	parentNoteRead = models.BooleanField()
	parentApproval = models.BooleanField()
	advisorApproval = models.BooleanField()
	activation_key = models.CharField(max_length=40, blank = True, null = True)
	objects = UserManager()
        def __unicode__(self):
	        return u'%s %s %s' %(self.first_name, self.last_name, self.username)

class StudentHouseParent (models.Model):
	studentIDNumber = models.IntegerField()
	houseID = models.IntegerField()
	parentStudentID = models.ForeignKey(ParentStudent,blank = True, null = True)
        def __unicode__(self):
	        return u'%s %s %s' %(self.studentIDNumber, self.houseID, self.parentStudentID)

class Discipline (models.Model):
	discipline_Choices= (
		('Math', 'Math'),
		('Science', 'Science'),
		('English', 'English'),
		('History', 'History'),
		('Language', 'Language'),
		('PE', 'PE'),
		('Visual Art','Visual Art'),
		('Dance','Dance'),
		('Computer Science','Computer Science'),
		('Music','Music'),
		('Misc','Misc'),
		('Theater', 'Theater')
	)
	discipline = models.CharField(max_length=16, choices= discipline_Choices)
	departmentChair = models.ForeignKey(User, limit_choices_to={'groups__in': [1]})
        def __unicode__(self):
	        return u'%s %s %s' %(self.discipline, self.departmentChair.first_name, self.departmentChair.last_name)

class Course (models.Model):
	courseNumber = models.IntegerField(db_index=True, max_length=9, primary_key=True)
	courseName = models.CharField(db_index=True, max_length=256)
	courseDescription = models.TextField(max_length = 65000, blank = True, null = True)
	preapprovalRequired = models.BooleanField()
	gradesOffered = models.CommaSeparatedIntegerField(max_length=16)
	prerequisite = models.CharField(max_length = 2000, blank = True, null = True)
	corequisite = models.CharField(max_length = 2000, blank = True, null = True)
	courseCredit = models.CharField(max_length = 200, blank = True, null = True)
	level = models.IntegerField(blank = True, null = True)
	rankChoices = (
		('EngHist', 'EngHist'),
		('English', 'English'),
	)

	rankType = models.CharField(max_length=10, choices = rankChoices, blank = True, null = True)
        def __unicode__(self):
	        return u'%s' %(self.courseName)

class CourseDiscipline (models.Model):
	courseID = models.ForeignKey(Course)
	discipline = models.ForeignKey(Discipline)
        def __unicode__(self):
	        return u'%s %s' % (self.courseID, self.discipline.discipline)

class Section (models.Model):
	courseID = models.ForeignKey(Course, db_index=True)
	sectionNumber = models.CharField(max_length = 12)
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
	#RoomNumber
        def __unicode__(self):
	        return u'%s %s' % (self.courseID, self.id)


class StudentSchedule (models.Model):
	studentID= models.ForeignKey(Student)
	sectionID= models.ForeignKey(Section)
	rank = models.IntegerField(null=True, blank=True)
	alternateFor = models.ForeignKey(Course, null=True, blank=True)#studSched
	conflictMessage = models.CharField(max_length = 10000, blank = True, null = True)
        def __unicode__(self):
	        return u'%s %s' % (self.studentID, self.sectionID)
	        	
class PreApproval (models.Model):
	studentID = models.ForeignKey(Student)
	courseID = models.ForeignKey(Course, limit_choices_to={'preapprovalRequired': True})
        def __unicode__(self):
	        return u'%s %s' % (self.studentID, self.courseID)

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
		return u'%s' % (self.message)

class AlternateCourse(models.Model):
	courseID = models.ForeignKey(Course)
	grade = models.CharField(max_length=16, choices= gradeChoices)
	def __unicode__(self):
		return u'%sth Grade %s' % (self.grade, self.courseID)