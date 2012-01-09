from django.db import models

class House (models.Model):
	houseAdvisorOne_firstName = models.CharField(max_length=128)
	houseAdvisorOne_lastName = models.CharField(max_length=128)
	houseAdvisorTwo_firstName = models.CharField(max_length=128)
	houseAdvisorTwo_lastName = models.CharField(max_length=128)
	roomNumber = models.IntegerField()
	studentNumber = models.IntegerField()

class Parent (models.Model):
	parentFirstName= models.CharField(max_length=128)
	parentLastName= models.CharField(max_length=128)
	parentEmail = models.CharField(max_length=256) 
	parentPhoneNumber = models.IntegerField()
	
class ParentStudent (models.Model):
	parentOneID = models.ForeignKey(Parent, related_name =' parent_one')
	parentTwoID = models.ForeignKey(Parent, related_name =' parent_two')
	

class Student (models.Model):
	firstName = models.CharField(max_length=128)
	lastName= models.CharField(max_length=128)
	email = models.EmailField()
	password= models.CharField(max_length=128)
	grade= models.IntegerField()
	houseID= models.ForeignKey(House)
	parentStudentID= models.ForeignKey(ParentStudent)


class DepartmentChair (models.Model):
	email= models.EmailField()
	firstName = models.CharField(max_length=128)
	lastName = models.CharField(max_length=128)	

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
	)
	discipline = models.CharField(max_length=16, choices= discipline_Choices)
	departmentChair = models.ForeignKey(DepartmentChair)

class Course (models.Model):
	courseName = models.CharField(max_length=256)
	courseDescription = models.CharField(max_length=2048)
	preapprovalRequired = models.BooleanField()
	discipline = models.ForeignKey(Discipline)
	grades_Offered = models.CommaSeparatedIntegerField(max_length=16)

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

class StudentSchedule (models.Model):
	studentID= models.ForeignKey(Student)
	sectionID= models.ForeignKey(Section)
	rank = models.IntegerField()
	
class PreApproval (models.Model):
	studentID = models.ForeignKey(Student)
	courseID = models.ForeignKey(Course)
