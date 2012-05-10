from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.db.models import Q
from registrationApp.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.core.mail import send_mass_mail
from django.http import Http404
import ldap

from operator import itemgetter
import re, random, sha, csv
from datetime import datetime
#import time

'''
def xls_to_response(xls, fname):
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    xls.save(response)
    return response
'''


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)

@login_required
def test(request):
	response = HttpResponse(mimetype='text/csv')
	response['Content-Disposition'] = 'attachment; filename=somefilename.csv'
	writer = csv.writer(response)
	students = Student.objects.all()
	for student in students:
		studentSchedule = StudentSchedule.objects.filter(studentID = student.id)
		for studSched in studentSchedule:
			writer.writerow([student.id, student.first_name,studSched.sectionID.courseID, studSched.sectionID, studSched.rank, studSched.alternateFor.courseName ])
	return response

def daysToPeriod(section):
	periods = ""
	pAndD = []
	days = []
	sectionPeriods = section.__dict__
	for period, day in sorted(sectionPeriods.iteritems()):
		if "PeriodDays" in period and day:
			days.append(day)
			pAndD.append((period[0], day, len(day)))

	pAndD.sort(key=itemgetter(2), reverse = True)
	for p, d, l in pAndD:
		periods += p
	return periods, days

def preApprovalCheck(student, course, preApprovals):
	preApproved = False
	for preApp in preApprovals:
		if preApp.courseID == course:
			preApproved = True
	return preApproved

@login_required
@group_required('student')
def printSchedule(request):
	student = get_object_or_404(Student, pk= request.user.id)

	#for student in students:
	fullYearCourses = []
	rankedCourses = []
	alternateCourses = []
	alternateRankedCourses = []
	otherCourses = []
	grade = abs(student.graduationYear - datetime.now().year - 13)
	studentInfo = {'First Name':student.first_name, 'Last Name': student.last_name, 'ID #':student.id, 'Grade':grade}

	preApprovals = PreApproval.objects.filter(studentID = student.id)
	studentSchedule = StudentSchedule.objects.filter(studentID = student)

	for studSched in studentSchedule:
		course = studSched.sectionID.courseID
		disciplines = CourseDiscipline.objects.filter(courseID = course)
		period, days = daysToPeriod(studSched.sectionID)
		if course.preapprovalRequired:
			preApproved = preApprovalCheck(student, course, preApprovals)
		else:
			preApproved = False

		if studSched.sectionID.semesterOne and not studSched.sectionID.semesterTwo:
			semester = "First Semester"
		elif studSched.sectionID.semesterTwo and not studSched.sectionID.semesterOne:
			semester = "Second Semester"
		else:
			semester = "Year"
		if studSched.sectionID.semesterOne and studSched.sectionID.semesterTwo and not studSched.alternateFor and not course.rankType=="English" and not course.rankType=="EngHist":
			fullYearCourses.append((disciplines, course.courseNumber, course.courseName, period, preApproved))

		elif not course.rankType=="EngHist" and not course.rankType=="English" and not studSched.alternateFor:
			otherCourses.append((disciplines, course.courseNumber, course.courseName, period, preApproved, semester))

		if grade == 12 and course.rankType == "EngHist" and not studSched.alternateFor:
			rankedCourses.append((studSched.rank, course.courseNumber, course.courseName, period, semester))
				
		if grade == 11 and course.rankType == "English" and not studSched.alternateFor:
			rankedCourses.append((studSched.rank, course.courseNumber, course.courseName, period, semester))
		
		if grade == 12 and course.rankType == "EngHist" and studSched.alternateFor:
			alternateRankedCourses.append((studSched.rank, course.courseNumber, course.courseName, period, studSched.alternateFor, semester))

		elif grade == 11 and course.rankType == "English" and studSched.alternateFor:
			alternateRankedCourses.append((studSched.rank, course.courseNumber, course.courseName, period, studSched.alternateFor, semester))
		
		elif studSched.alternateFor:
			alternateCourses.append((course.courseNumber, course.courseName, period, studSched.alternateFor, semester))
	
	rankedCourses.sort(key=itemgetter(0))
	return render_to_response('registrationApp/output.html', {'studentInfo': studentInfo, 'fullYearCourses': fullYearCourses, 'rankedCourses':rankedCourses, 'alternateCourses': alternateCourses, 'alternateRankedCourses': alternateRankedCourses, 'otherCourses':otherCourses},
							    context_instance=RequestContext(request))


def requiredCheck(student, studentSchedule):
	required = RequiredObjects.objects.filter(grade = (abs(student.graduationYear - datetime.now().year - 13)))
	requiredBoolList = []
	for req in required:
		reqPass = False
		for studSched in studentSchedule:
			if studSched.sectionID.courseID == req.courseID:
				reqPass = True
			else:
				disc = CourseDiscipline.objects.filter(courseID = studSched.sectionID.courseID.courseNumber)
				for discipline in disc:
					if req.discipline == discipline.discipline:
						reqPass = True
		requiredBoolList.append((req, reqPass))
	return requiredBoolList

@login_required
@group_required('student')
def index(request):
	student = get_object_or_404(Student, pk= request.user.id)
	return render_to_response('registrationApp/search.html', {'student': student},
							    context_instance=RequestContext(request))

def split_into_keywords(query_string,
                   	findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\section{2,}').sub): 
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    query = None       
    terms = split_into_keywords(query_string)
    for term in terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def daysToPeriod(section):
	periods = ""
	pAndD = []
	daysUnordered = []
	sectionPeriods = section.__dict__
	for period, day in sorted(sectionPeriods.iteritems()):
		if "PeriodDays" in period and day:
			daysUnordered.append(day)
			pAndD.append((period[0], day, len(day)))

	pAndD.sort(key=itemgetter(2), reverse = True)
	days=[]
	for p, d, l in pAndD:
		periods += p
		days.append(d)
	return periods, days

def numbersToDay(numbers):
	output = ""
	for num in sorted(numbers):
		lists = [x.strip() for x in num.split(',')]
		for day in lists:
			if int(day) == 1:
				output += "M, "
			if int(day) == 2:
				output += "T, "
			if int(day) == 3:
				output += "W, "
			if int(day) == 4:
				output += "R, "
			if int(day) == 5:
				output += "F1 "
			if int(day) == 6:
				output += "F2, "
			if int(day) == 7:
				output += "F3, "
			if int(day) == 8:
				output += "F4, "
	return output[:-1] #["-2"]


def checkPeriodMatch(section, existingSection):
	canAdd = True
	conflicts = []
	sectionPeriods = section.__dict__
	existingSectionPeriods = existingSection.__dict__
	for t, existingT in zip(sorted(sectionPeriods.iteritems()), sorted(existingSectionPeriods.iteritems())):
		period = t[0]
		existingPeriod = existingT[0]
		if "PeriodDays" in period and "PeriodDays" in existingPeriod:
			if t[1] and existingT[1]:
				listA = [x.strip() for x in t[1].split(',')]
				listB = [x.strip() for x in existingT[1].split(',')]
				match = list(set(listA) & set(listB))
				if match:
					canAdd = False
					conflicts.append((period[0], match))
	return  canAdd, conflicts


def checkPeriodAvailable(studentSchedule, course = None, section = None):
	if section is not None:
		sectionOptions = Section.objects.filter(pk = section.id)
	elif course is not None:
		sectionOptions = Section.objects.filter(courseID = course)
	conflict = []
	sectionToAdd = None
	conflictListAll = []
	sectionAddable = False
	for section in sectionOptions:
		canAddList = []
		for existingSection in studentSchedule:
			canAdd, conflict = checkPeriodMatch(section, existingSection.sectionID)
			canAddList.append((canAdd, conflict, section, existingSection.sectionID))
		if all([(canAddList[i][0]) for i in range(len(canAddList))]):
			sectionToAdd = section
			sectionAddable = True
		else:
			conflictList = []
			for canAdd, conflict, section, existingSection in canAddList:
				for x, y in conflict:
					conflictList.append((section, existingSection, x, y))
 			conflictListAll.append((conflictList, sum([len(u) for e, r, t, u in conflictList])))
	conflictListAll.sort(key=itemgetter(1))
	if conflictListAll and not sectionAddable:
		conflict = conflictListAll[0][0]
	return sectionToAdd, conflict

def sectionConflictPeriodCheck (student, studentSchedule, course= None, section=None):
	msg = ""
	add =  False
	sec = ""
	
	if section is not None:
		sectionToAdd, conflict = checkPeriodAvailable(studentSchedule, section=section)
		courseName = section.courseID.courseName
	elif course is not None:
		sectionToAdd, conflict = checkPeriodAvailable(studentSchedule, course = course)
		courseName = course.courseName


	if sectionToAdd is not None:
		add = True	
	else:
		for count, (sec, existingSection, periodConflict, dayConflict) in enumerate(conflict):
			period, days = daysToPeriod(existingSection)
			secPeriod, secDays = daysToPeriod(sec)
			daysConflict = numbersToDay(dayConflict)
			if len(conflict) == (count + 1) :
				msg += courseName +  " " + secPeriod + " Period conflicts with " + existingSection.courseID.courseName+ " " + period + " Period on " + daysConflict +  " during " + periodConflict +"."
			else:
				msg += courseName +  " " + secPeriod + " Period conflicts with " + existingSection.courseID.courseName+ " " + period + " Period on " + daysConflict +  " during " + periodConflict + " and, additionally, "

	return add, sectionToAdd, msg, sec

def gradeCheck(student, course):
	gradesOffered = str(course.gradesOffered)
	lis = [x.strip() for x in gradesOffered.split(',')]
	for l in lis:
		if (student.graduationYear - datetime.now().year)  == (13 - int(l)):
			availForGrade = True
			break
		else:
			availForGrade = False	
	return availForGrade

def alreadyEnrolledCourse(student, course, studentSections):
	alreadyEnrolledCourse = False
	sectionEnrolled = []
	
	for studSched in studentSections:
		if studSched.sectionID.courseID == course:
			alreadyEnrolledCourse = True
			sectionEnrolled.append(studSched.sectionID)
	return alreadyEnrolledCourse, sectionEnrolled


@login_required
@group_required('student')
def searchResults(request):
    #from django.db import connection, transaction

	t = get_object_or_404(Student, id=request.user.id)
	if request.is_ajax():
		#zero= time.clock()

		searchTerms = request.POST.get('q')
		onlyDisciplineSearch = request.POST.get('onlyDisciplineSearch')
		courseOptions = []
		rank = []
		courseList = []                                        
		preApproved = True
    	#cursor = connection.cursor()
       	#cursor.execute('SELECT courseNumber FROM registrationApp_course where MATCH(courseName, courseDescription) AGAINST ("c*" in boolean mode)')
       	#found = cursor.fetchall()
   		#found = Course.objects.raw('SELECT courseNumber FROM registrationApp_course where MATCH(courseName, courseDescription) AGAINST ("c*" in boolean mode)')
		found = get_query((searchTerms), ['courseNumber','courseName', 'courseDescription', 'coursediscipline__discipline__discipline'])
        if found is not None:
        	
        	if onlyDisciplineSearch == "1":
        		courseOptions = Course.objects.filter(coursediscipline__discipline__discipline = str(searchTerms))
        		
        	else:
        		courseOptions = Course.objects.select_related().filter(found).distinct() #select related would be more helpful with foreign keys
        	studentSections = StudentSchedule.objects.filter(studentID = t.id)
        	preApprovals = PreApproval.objects.filter(studentID = t.id)
        	required = RequiredObjects.objects.filter(grade = (abs(t.graduationYear - datetime.now().year - 13)))

        	for course in courseOptions:
				discipline =""
				rankScore = 0

				discipline = CourseDiscipline.objects.select_related().filter(courseID = course.courseNumber)

				p = re.compile('%s*'% unicode(searchTerms).lower())
				m = p.match(unicode(course.courseName).lower())
				if m:
					rankScore +=50
				if unicode(searchTerms).lower() == unicode(course.courseName).lower():
					rankScore += 200
					
				for disc in discipline:
					if  unicode(searchTerms).lower() in unicode(disc.discipline).lower():
						rankScore += 10
					if  unicode(searchTerms).lower() == unicode(disc.discipline).lower():
						rankScore += 50
				
				availForGrade = gradeCheck(t, course)
				
				if  availForGrade:
					rankScore += 10
				else:
					rankScore -= 200

				if course.preapprovalRequired:
					preApproved = preApprovalCheck(t, course, preApprovals)
					if preApproved:
						rankScore += 30
					else:
						rankScore -= 300

				alreadyEnrolledinCourse, sectionEnrolled = alreadyEnrolledCourse(t, course, studentSections)
				if alreadyEnrolledinCourse:
					rankScore -= 20 
				for req in required:
					if course == req.courseID:
						rankScore += 20
					else:
						for disc in discipline:
							if disc.discipline == req.discipline:
									rankScore += 20

				'''
				requiredBoolList = requiredCheck(t, studentSections)
				for req, reqPass in requiredBoolList:
					if not reqPass:
						if course == req.courseID:
							rankScore += 20
						else:
							for disc in discipline:
								if disc.discipline == req.discipline:
									rankScore += 20
				'''
				sectionOptions = Section.objects.filter(courseID = course.courseNumber)
				sections = []
			
				for section in sectionOptions:
					period, day = daysToPeriod(section)
					sections.append((section, period, day))

				courseList.append((course, rankScore, sections, availForGrade, preApproved, discipline))

				courseList.sort(key=itemgetter(1), reverse = True)
		#ab= time.clock() - zero
		#return HttpResponse(ab)
		return render_to_response('registrationApp/searchResults.html', {'student': t, 'courseList' : courseList, 'searchTerms': searchTerms},
										context_instance=RequestContext(request))			
	else:
		return HttpResponse(" ")


def periodSwitch (studentSchedule):
	secOption = []
	sectionOptions = []
	for studSched in studentSchedule:
		output =[]
		sectionOptions = Section.objects.filter(courseID = studSched.sectionID.courseID)
		for s in sectionOptions:
			output.append(s)
		secOption.append(output)
	return (secOption)

def alreadyEnrolledSection(student, section):
	alreadyEnrolled = False
	studentSections = StudentSchedule.objects.filter(studentID = student)
	for studSched in studentSections:
		if studSched.sectionID == section:
			alreadyEnrolled = True
	return alreadyEnrolled
	
def studentScheduleAddView(studentSchedule, student):
	engHistRank = []
	engRank = []
	studSched = []
	grade = abs(student.graduationYear - datetime.now().year - 13) #TODO: This Should Be System Property 

	for sectionList in studentSchedule:
		discipline = CourseDiscipline.objects.filter(courseID = sectionList.sectionID.courseID.courseNumber)
		prd, dayz = daysToPeriod(sectionList.sectionID)

		sectionOptions = Section.objects.filter(
			courseID = sectionList.sectionID.courseID
			).exclude(pk = sectionList.sectionID.id
		)
		
		sectionsOptions = []
		for section in sectionOptions:	
			append = True
			for s in studentSchedule:
				if section == s.sectionID:
					append = False
			if append == True:
				period, days = daysToPeriod(section)
				sectionsOptions.append((section, period, days))

		droppable = False 
		alternateRequired = AlternateCourse.objects.filter(grade = grade)
		for alternate in alternateRequired:
			if alternate.courseID == sectionList.sectionID.courseID:
				droppable = True

		show = True
		if sectionList.alternateFor:	
			for studentScheduleObj in studentSchedule:
				if sectionList.alternateFor.courseNumber == studentScheduleObj.sectionID.courseID.courseNumber:
					show = False

		studSched.append((sectionList, prd, discipline, sectionsOptions, sectionList.rank, dayz, droppable, show))
		studSched.sort(key=itemgetter(1))

	return studSched

def addSection(student, section):
	studSchedule, created= StudentSchedule.objects.get_or_create(
						studentID = student, sectionID=section)
	if created:
		period, days = daysToPeriod(studSchedule.sectionID)
		msg = studSchedule.sectionID.courseID.courseName +" " + period + " Period Added "
	else: 
		msg = "Could not add "
	return msg

@login_required
@group_required('student')
def add(request):
	#student = request.POST.get('student')
	#if student is not None:
	#	u = get_object_or_404(Student, id = student)
	#else:
	u = get_object_or_404(Student, id=request.user.id)
	section = ""
	confirmationBox = []
	messageType = ""
	msg = []
	if u.submit:
		msg.append("You've already submitted!")

	elif request.is_ajax():
		sec = request.POST.get('section')
		confirm = request.POST.get('confirm')
		if confirm:
			confirm = int(confirm)
		else:
			confirm = 0
		if sec is None:
			course = request.POST.get('course')
			if course is not None:
				courseObj = Course.objects.get(pk = course)
				sSched = StudentSchedule.objects.filter(studentID = u.id)
				add, sectionAdd, message, sect = sectionConflictPeriodCheck(u, sSched, course = courseObj)

				if add:
					msg.append(addSection(u, sectionAdd))
					messageType = "success"
				elif not add and confirm ==1:
					msg.append(addSection(u, sect))
					messageType = "success"
				elif not add:
					confirmationBox = [[True, courseObj]]
					msg.append(message)
					messageType = "warning"


		if sec:
			try:
				section = Section.objects.get(pk=sec)
			except ValueError:
				pass
			continues = True

			if section is not None:

				alreadyEnrolled = alreadyEnrolledSection(u, section)
				if alreadyEnrolled:
					period, days = daysToPeriod(section)
					msg.append("You are already enrolled in section " + period + " of " + section.courseID.courseName +".")
					continues = False
					messageType = "error"

				elif section.courseID.preapprovalRequired:
					preApprovals = PreApproval.objects.filter(studentID = u.id)

					preApproved = preApprovalCheck(u, section.courseID, preApprovals)
					if not preApproved:
						msg.append("You are not preapproved for " + str(section.courseID.courseName) +".")
						continues = False
						messageType = "error"
				if continues:
					
					availForGrade = gradeCheck(u, section.courseID)
				
					if availForGrade or (not availForGrade and confirm == 1):
						continues = True

					elif not availForGrade and confirm ==0:
						msg.append(section.courseID.courseName +" is not available for your grade. ")
						confirmationBox = [[True, ""]]
						continues = False
						messageType = "warning"
					sSched = StudentSchedule.objects.filter(studentID = u.id)
					alreadyEnrolledC, sectionEnrolled = alreadyEnrolledCourse(u, section.courseID, sSched)

					periods = ""
					for sections in sectionEnrolled:
						period, days= daysToPeriod(sections)
						periods += period
						
					if continues and (not alreadyEnrolledC or (alreadyEnrolledC and confirm == 1)):
						continues = True

					elif alreadyEnrolledC and confirm == 0:
						msg.append("You are already enrolled in section " + periods + " of " + Section.objects.get(pk=sec).courseID.courseName+"." )
						confirmationBox = [[True, ""]]
						continues = False
						messagetype = "warning"
						
					
					add, sectionAdd, mess, sect = sectionConflictPeriodCheck(u, sSched, section = section)

					if add and continues:
						msg.append(addSection(u, sectionAdd))
						messageType = "success"
					elif continues and not add and confirm ==1: 	
						msg.append(addSection(u, section))
						messageType = "success"
					elif not add:
						confirmationBox = [[True, ""]]
						msg.append(mess)
						messageType = "warning"

	studentSchedule = StudentSchedule.objects.filter(studentID = u)

	requiredBoolList = requiredCheck(u, studentSchedule)
	reqMessage = []
	for req, reqPass in requiredBoolList:
		if not reqPass:
			reqMessage.append((req, req.message))


	studentSchedules = studentScheduleAddView(studentSchedule, u)
	return render_to_response('registrationApp/add.html', {'student': u, 'studentSchedules': studentSchedules, 'section': section, 'msg' : msg, 'reqMessage' : reqMessage, 'confirmationBox': confirmationBox, 'messageType' : messageType},
								context_instance=RequestContext(request))		

	'''
							studentSchedule = StudentSchedule.objects.filter(studentID = u)
							if section.courseID.rankType:
								engHistCount = 1
								engCount = 1
								for sectionList in studentSchedule:
									if str(sectionList.sectionID.courseID.rankType) == "EngHist":
										engHistCount = engHistCount + 1
									elif str(sectionList.sectionID.courseID.rankType) == "English":
										engCount = engCount + 1
								if engHistCount > 1:
									rank = engHistCount
								elif engCount > 1:
									rank = engCount
								else:
									rank = 1
							else: rank = 1 	
		'''

def studentSchedule(request):
	stud = request.POST.get('student')
	if stud:
		student = get_object_or_404(Student, id = stud)
	else:
		student = get_object_or_404(Student, id = request.user.id)

	fromOther = request.POST.get('fromOther')
	cover = True		
	
	if fromOther is not None:
		if int(fromOther) == 1:
			cover = False

	sSched = StudentSchedule.objects.filter(studentID = student.id)
	studentSchedule = studentScheduleAddView(sSched, student)
	requiredBoolList = requiredCheck(student, sSched)
	reqMessage = []
	for req, reqPass in requiredBoolList:
		if not reqPass:
			reqMessage.append((req, req.message))

	return render_to_response('registrationApp/studentSchedule.html', {'student': student, 'studentSchedule': studentSchedule, 'reqMessage' : reqMessage,'cover':cover},
								context_instance=RequestContext(request))


@login_required
@group_required('student')						 
def delete(request):
	rank = 0 
	msg= []
	messageType = ""

	z = get_object_or_404(Student, id=request.user.id)
	if request.is_ajax():
		studSched = request.POST.get('studSched')
		try:
			studSchedObj = StudentSchedule.objects.get(pk = studSched)
			studentSchedule = StudentSchedule.objects.filter(studentID = z)

			if studSchedObj is not None:
				if studSchedObj.rank:
					deletedRankType = studSchedObj.sectionID.courseID.rankType
					deletedRank = studSchedObj.rank
					for studSchedule in studentSchedule:
						if studSchedule.sectionID.courseID.rankType == deletedRankType:
							if deletedRank < studSchedule.rank:
								studSchedule.rank = studSchedule.rank - 1
								studSchedule.save()
				for studSchedule in studentSchedule:
					if studSchedule.alternateFor == studSchedObj.sectionID.courseID:
						studSchedule.alternateFor = None
						studSchedule.save()

				
				studSchedObj.delete()
				messageType = "success"
				msg.append(studSchedObj.sectionID.courseID.courseName + " Deleted")
				
			else:
				messageType = "error"
				msg.append("Could not delete; " + studSchedObj.sectionID.courseID.courseName +" does not exist")
		except StudentSchedule.DoesNotExist:
			msg.append("Already Deleted")
		studentSchedule = StudentSchedule.objects.filter(studentID = z)
		secOption = periodSwitch(studentSchedule)
		fromOtherBool = False
		requiredBoolList = requiredCheck(z, studentSchedule)
		reqMessage = []
		for req, reqPass in requiredBoolList:
			if not reqPass:
				reqMessage.append((req, req.message))
		studentSchedules = studentScheduleAddView(studentSchedule, z)
		return render_to_response('registrationApp/add.html', {'student': z, 'studentSchedules': studentSchedules, 'msg': msg, 'fromOtherBool' : fromOtherBool,'reqMessage' : reqMessage, 'messageType': messageType},
							   			context_instance=RequestContext(request))	


@login_required
@group_required('student')
def notifications(request):
	student = get_object_or_404(Student, id=request.user.id)
	if request.is_ajax():
		full = False
	else:
		full = True
	return render_to_response('registrationApp/notifications.html',{'student': student, 'full': full, 'notifDiv': True},
								context_instance=RequestContext(request))

@login_required
@group_required('student')
def notifRead(request):
	stud = get_object_or_404(Student, id=request.user.id)
	if request.is_ajax():
		notes = request.POST.get('note')
		notes = notes.split(",")
		for note in notes:
			if note == "advisorNote":
				stud.advisorNoteRead = 1
				stud.save()
			if note == "parentNote":
				stud.parentNoteRead = 1
				stud.save()	
	return HttpResponse("Notifications Marked as Read")

@login_required
@group_required('student')
def catalog(request):
	a = get_object_or_404(Student, id=request.user.id)
	courses = Course.objects.all()
	name = []
	desc = []
	for c in courses:
		name.append(c.courseName)
		name.append("<br><br><br><br><br><br><br><br>")
		desc.append(c.courseDescription)
	return render_to_response('registrationApp/courseCatalog.html', {'student': a, 'courses' :courses})

@login_required
@group_required('student')
def one (request):
	sections = []
	student = get_object_or_404(Student, id= request.user.id)
	grade = abs(student.graduationYear - datetime.now().year - 13)
	studentSchedule = StudentSchedule.objects.filter(studentID = student)
	requiredBoolList = requiredCheck(student, studentSchedule)
	requiredList = []
	for req, reqPass in requiredBoolList:
		requiredList.append((req, reqPass, req.message))
	sections = studentScheduleAddView(studentSchedule, student)
	preApprovals = []
	preApproval = PreApproval.objects.filter(studentID = student.id)
	for preApp in preApproval:
		disciplines = CourseDiscipline.objects.filter(courseID = preApp.courseID)
		preApprovals.append((preApp,disciplines))
	return render_to_response('registrationApp/one.html', {'student': student, 'grade': grade, 'sections'  : sections, 'requiredList': requiredList, 'preApprovals': preApprovals},
								context_instance=RequestContext(request))

@login_required
@group_required('student')
def preferences (request):
	student = get_object_or_404(Student, id= request.user.id)
	grade = abs(student.graduationYear - datetime.now().year - 13) #TODO: This Should Be System Property 
	studentSchedule = StudentSchedule.objects.filter(studentID = student).order_by('rank')
	alternateRequired = AlternateCourse.objects.filter(grade = grade)
	alternateCourseRequired = []
	for alternate in alternateRequired:
		for section in studentSchedule:
			if alternate.courseID == section.sectionID.courseID:
				discipline = CourseDiscipline.objects.filter(courseID = section.sectionID.courseID.courseNumber)
				alternates = []
				for studSched in studentSchedule:
					if studSched.alternateFor == section.sectionID.courseID:
						disciplinez = CourseDiscipline.objects.filter(courseID = studSched.sectionID.courseID.courseNumber)
						alternates.append((studSched, disciplinez))
				alternateCourseRequired.append((section, discipline, alternates))

	sections = studentScheduleAddView(studentSchedule, student)
	engHist = []
	english = []
	for studSched, prd, disciplines, sectionOptions, rank, dayz, droppable, show in sections:
		if not studSched.alternateFor:
			if studSched.sectionID.courseID.rankType == "EngHist":
				engHist.append((studSched, prd, disciplines, rank))
			elif studSched.sectionID.courseID.rankType == "English":
				english.append((studSched, prd, disciplines, rank))
	engHist.sort(key=itemgetter(3))
	english.sort(key=itemgetter(3))
	return render_to_response('registrationApp/preferences.html', {'student': student, 'grade': grade, 'engHist'  : engHist, 'english'  : english, "alternateCourseRequired" : alternateCourseRequired},
								context_instance=RequestContext(request))

@login_required
@group_required('student')
def alternate(request):
	student = get_object_or_404(Student, id=request.user.id)
	if request.is_ajax():
		alternatePOST = request.POST.get('alternateID')
		alternateForPOST = request.POST.get('alternateFor')
		alternate = StudentSchedule.objects.get(pk = alternatePOST)
		alternateForStudSched = StudentSchedule.objects.get(pk = alternateForPOST)
		alternateFor = Course.objects.get(courseNumber = alternateForStudSched.sectionID.courseID.courseNumber)
		alternate.alternateFor = alternateFor
		alternate.save()
		if alternate.alternateFor == alternateFor:
			return HttpResponse("Alternate Saved Successfully")
		
@login_required
@group_required('student')
def rankChange(request):
	student = get_object_or_404(Student, id=request.user.id)
	if request.is_ajax():
		rankOrder = request.POST.get('rankOrder')
		rankOrderList = rankOrder.split("&")
		for count, studSched in enumerate(rankOrderList):
			studSched = StudentSchedule.objects.get(pk = studSched[7:])
			studSched.rank = count + 1
			studSched.save()
  	return HttpResponse("Order Saved!")

@login_required
@group_required('student')
def schedule(request): #this goes to the schedule view
	student = get_object_or_404(Student, id = request.user.id)
	studentSchedule = StudentSchedule.objects.filter(studentID = student.id)
	schedule = []
	for studSched in studentSchedule:
		sectionPeriods = studSched.sectionID.__dict__
		for period, day in sorted(sectionPeriods.iteritems()):
			if "PeriodDays" in period and day:
				schedule.append((studSched.sectionID.courseID.courseName, period[0], day))
				#appends courseName, period Letter, day in 1,2,3,4,5,6,7,8 format, where 1-4 is m-t, and 5-8 is a friday 
				#days = numbersToDay(numbers) to change 1,2,3 to M,T,W
	return HttpResponse (schedule)

def warnings(student, studentSchedule):
	warnings = []
	for studSched in studentSchedule:
		#ALTERNATES/RANKINGS

		conflictMessage = ""
		availForGrade = gradeCheck(student, studSched.sectionID.courseID)
		if not availForGrade:
			conflictMessage += studSched.sectionID.courseID.courseName + " is not available for " + str(abs(student.graduationYear - datetime.now().year - 13)) +"th grade."
		sSched = StudentSchedule.objects.filter(studentID = student.id).exclude(pk = studSched.id)

		alreadyEnrolledC, sectionEnrolled = alreadyEnrolledCourse(student, studSched.sectionID.courseID, sSched)

		periods = ""
		for sections in sectionEnrolled:
			period, days= daysToPeriod(sections)
			periods += period

		if alreadyEnrolledC:
			conflictMessage += student.first_name +" " + student.last_name +" is already enrolled in section " + periods + " of " + studSched.sectionID.courseID.courseName+"." 

		add, sectionAdd, mess, sect = sectionConflictPeriodCheck(student, sSched, section = studSched.sectionID)
		if not add:
			conflictMessage += mess


		if conflictMessage is not "":
			studSched.conflictMessage = conflictMessage
			studSched.save()
			warnings.append((studSched.sectionID.courseID.courseName, conflictMessage))
	return warnings

def warningOutput(request):
	stud = request.POST.get('student')
	if stud:
		student = get_object_or_404(Student, id = stud)
	else:
		student = get_object_or_404(Student, id = request.user.id)

	studentSchedule = StudentSchedule.objects.filter(studentID = student.id)
	warning = warnings(student, studentSchedule)
	requiredBoolList = requiredCheck(student, studentSchedule)
	reqMessage = []
	for req, reqPass in requiredBoolList:
		if not reqPass:
			reqMessage.append((req, req.message))
	return render_to_response('registrationApp/warningOutput.html', {'warning': warning, 'reqMessage': reqMessage})

def parentNamesandEmails(studentHouseParent):
	parents = studentHouseParent.parentStudentID.parentOneID.parentFirstName + " " +studentHouseParent.parentStudentID.parentOneID.parentLastName
	parentEmails = []
	parentOneEmail = studentHouseParent.parentStudentID.parentOneID.parentEmail
	parentEmails.append(parentOneEmail)
	if studentHouseParent.parentStudentID.parentTwoID:
		parents += " and " +studentHouseParent.parentStudentID.parentTwoID.parentFirstName + " " + studentHouseParent.parentStudentID.parentTwoID.parentLastName
		parentTwoEmail = studentHouseParent.parentStudentID.parentTwoID.parentEmail
		parentEmails.append(parentTwoEmail)
	return (parents, parentEmails)

def advisorNamesandEmails(studentHouseParent):
	house = House.objects.get(pk = studentHouseParent.houseID)
	advisors = house.houseAdvisorOneID.first_name + " " + house.houseAdvisorOneID.last_name
	advisorEmails = []
	advisorOneEmail = house.houseAdvisorOneID.email
	advisorEmails.append(advisorOneEmail)
	if house.houseAdvisorTwoID:
		advisors += " and " + house.houseAdvisorTwoID.first_name + " " + house.houseAdvisorTwoID.last_name
		advisorTwoEmail = house.houseAdvisorTwoID.email
		advisorEmails.append(advisorTwoEmail)
	return (advisors, advisorEmails)

@login_required
@group_required('student')
def submit(request):	
	student = get_object_or_404(Student, id=request.user.id)
	studentNote = request.POST.get('studentNote')
	studentSchedule = StudentSchedule.objects.filter(studentID = student.id)
	msg= ""
	if student.submit == True:
		msg.append("You have already submitted!")
	else:
		student.submit = True
		student.parentApproval = False
		student.advisorApproval = False
		student.studentNote = studentNote
		student.save()
		warning = warnings(student, studentSchedule)

		salt = sha.new(str(random.random())).hexdigest()[:5]
    	activation_key = sha.new(salt+student.first_name).hexdigest()
    	student.activation_key = activation_key
    	student.save()
    	try:
    		studentHouseParent = StudentHouseParent.objects.get(studentIDNumber = student.id)
	    	parents, parentEmails = parentNamesandEmails(studentHouseParent)
	    	advisors, advisorEmails = advisorNamesandEmails(studentHouseParent)
	    	parEmailBody = "Hello %s,\n \tYour child, %s %s, has submitted his/her schedule for your approval. Please follow this link to their schedule: http://compsci.dalton.org/registrationApp/ParentConfirm/%s" % (parents, student.first_name, student.last_name, student.activation_key)
	    	parentMessage = ("Your child has submitted his/her schedule. ", parEmailBody, '', parentEmails)
	    	advEmailBody = "Hello %s,\n \tYour advisee, %s %s, has submitted his/her schedule for your approval. Please log onto http://compsci.dalton.org/registrationApp/advisor/ to approve or to ask your advisee to make changes." % (advisors, student.first_name, student.last_name)
	    	advisorMessage =("Your advisee has submitted his/her schedule. ", advEmailBody, '', advisorEmails)
	    	send_mass_mail((parentMessage, advisorMessage), fail_silently=False)
	    	msg = "Submitted for House Advisor and Parent Approval"
    	except StudentHouseParent.DoesNotExist:
    		msg = "Submitted, but you have no parents and House Advisors in the database. "


	return HttpResponse(msg)

@login_required
@group_required('departmentChair')
def preapprovals(request):
	courses = []
	departmentChair = get_object_or_404(User, id = request.user.id)
	disciplines = Discipline.objects.filter(departmentChair = departmentChair)
	for discipline in disciplines:
		courseOptions = Course.objects.filter(coursediscipline__discipline__discipline = discipline.discipline, preapprovalRequired = True)
		courses.append(courseOptions)
	return render_to_response('registrationApp/preapprovals.html', {'departmentChair': departmentChair, 'courses': courses},
								context_instance=RequestContext(request))

@login_required
@group_required('departmentChair')
def preappContainer(request):
	departmentChair = get_object_or_404(User,  id = request.user.id)
	if request.is_ajax():
		courseID = request.POST.get('courseNumber')
		courseObj = Course.objects.get(pk = courseID)
	return render_to_response('registrationApp/preAppContainer.html', {'departmentChair': departmentChair, 'courseObj': courseObj},
								context_instance=RequestContext(request))

@login_required
@group_required('departmentChair')
def preappAdd(request):
	departmentChair = get_object_or_404(User,  id = request.user.id)
	msg = ""
	allCreated = True
	if request.is_ajax():
		courseID = request.POST.get('courseNumber')
		courseObj = Course.objects.get(pk = courseID)
		preAppName = request.POST.get('preappName')
		
		AD_LDAP_URL = 'ldap://directory89.dalton.org'
		AD_SEARCH_DN = 'OU=Dalton Users,DC=dalton,DC=org'
		AD_SEARCH_FIELDS = ['cn','mail','givenName','sn','sAMAccountName','description','employeeID','memberOf']
		AD_NT4_DOMAIN = 'dalton.org'
		ldap.set_option(ldap.OPT_REFERRALS,0) # DO NOT TURN THIS OFF OR SEARCH WON'T WORK!      
        l = ldap.initialize(AD_LDAP_URL)
        l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        binddn = "%s@%s" % ('c12dd', 'dalton.org')
        l.bind_s(binddn,'kti316u')
        preAppNames = [x.strip() for x in str(preAppName).split(',')]
        studentsAdded = []
        studentsNotAdded = []
        for preAppN in preAppNames:
			preAppSplitN = str(preAppN).split(' ')
			#students = Student.objects.filter(first_name__iexact = str(preAppSplitN[0]), last_name__iexact = str(preAppSplitN[1]))
			#if len(students) == 1:
				#for studentz in students:
					#student = Student.objects.get(id = studentz.id)
			baseDN = "OU=Dalton Users,DC=dalton,DC=org"
			searchScope = ldap.SCOPE_SUBTREE
			retrieveAttributes = None 
			a = ldap.initialize("ldap://directory89.dalton.org")
			a.protocol_version = ldap.VERSION3

			a.simple_bind('CN=Darshan Desai,OU=Students,OU=Dalton Users,DC=dalton,DC=org','kti316u')
			searchFilter = "(&(givenName=%s)(sn=%s))" % (str(preAppSplitN[0]), str(preAppSplitN[1]))

			result=a.search_s(baseDN,ldap.SCOPE_SUBTREE, searchFilter)[0][1]

			if result.has_key('mail'):
 				mail = result['mail'][0]
			else:
			    mail = None
			if result.has_key('employeeID'):
			    studID = result['employeeID'][0]
			else:
			    studID = None
			if result.has_key('sn'):
			    lastName = result['sn'][0]
			else:
			    lastName = None
			if result.has_key('givenName'):
			    firstName = result['givenName'][0]
			else:
			    firstName = None

			#preApp, created= PreApproval.objects.get_or_create(
			#studentID = studID, courseID=courseObj)
			subject = "You were preapproved for " + courseObj.courseName
			message = "Hello " + firstName + "; you were preapproved for " + courseObj.courseName + "."
			#if created == True:
			msg += firstName + " preapproval added <br> "
			send_mail(subject, message, '', [mail])
			msg += "Added " + firstName +  " " + lastName + " "
			studentsAdded.append((firstName, lastName))
			#elif created == False:
			#	msg += firstName + " is already preapproved <br> "
			#	allCreated = False
			#	msg += "Not Added " + firstName +  " " + lastName + " "
			#elif len(students) ==0:
			#	msg += "No student found for " + preAppN + " "
			#else:
			#	msg += "Multiple students found for " + preAppN + " "
			#if allCreated == True:
			#	msg += "All Added Successfully"
	return HttpResponse(msg)

@login_required
@group_required('houseAdvisor')
def advisor(request):
	houseAdvisor = get_object_or_404(User, id = request.user.id)
	house = House.objects.filter(houseAdvisorOneID = houseAdvisor)
	if house is None:
		house = House.objects.filter(houseAdvisorTwoID = houseAdvisor)
	house = House.objects.get(id = house)
	studentHouseParent = StudentHouseParent.objects.filter(houseID = house.id)

	students= []
	advisorApproved = []
	for studParHouse in studentHouseParent:
		student = Student.objects.get(pk = studParHouse.studentIDNumber)
		if student.parentApproval:
			students.append((student, True))
		elif not student.parentApproval:
			students.append((student, False))
		if student.advisorApproval:
			advisorApproved.append(student)

	students.sort(key=itemgetter(1), reverse = True)
	return render_to_response('registrationApp/advisor.html', {'house': house, 'students': students, 'advisorApproved':advisorApproved},
								context_instance=RequestContext(request))

@login_required
@group_required('houseAdvisor')
def approve(request):
	if request.is_ajax():
		msg = ""
		stud = request.POST.get('student')
		student = Student.objects.get(pk = stud)
		if student.submit:
			student.advisorApproval = True
			student.save()
			studentHouseParent = StudentHouseParent.objects.get(studentIDNumber = student.id)
	    	parents, parentEmails = parentNamesandEmails(studentHouseParent)
	    	parentEmails.append(student.email)
	    	emailSubject = "Advisor Approval of %s %s's Schedule" % (student.first_name, student.last_name)
	    	emailBody = "Hello; your advisor has approved your schedule! "
	    	send_mail(emailSubject, emailBody, '', parentEmails)
	    	msg = " %s %s's schedule was approved. Thank You!"%(student.first_name, student.last_name)
		if not student.submit:
			msg = "Student has not submitted!"
		return HttpResponse(msg)
	else:
		raise Http404

@login_required
@group_required('houseAdvisor')
def review(request):
	if request.is_ajax():
		student = request.POST.get('student')
		student = Student.objects.get(pk = student)
		message = request.POST.get('message')
		student.submit = False
		if student.advisorNote:
			note = message + " PREVIOUS NOTE: " + student.advisorNote
		else:
			note = message
		student.advisorNote = note
		student.advisorNoteRead = 0
		student.save()

		send_mail("Schedule Changes to review", "Hello; your advisor has some suggestions for you: " +message, '', [student.email])
	
	return HttpResponse("Message sent to %s %s successfully" %(student.first_name, student.last_name))

def parentReview(request):
	if request.is_ajax():
		student = request.POST.get('student')
		student = Student.objects.get(pk = student)
		if student.submit:
			message = request.POST.get('message')
			student.submit = False
			if student.parentNote:
				note = message + " PREVIOUS NOTE: " + student.parentNote
			else:
				note = message
			student.parentNote = note
			student.parentNoteRead = 0
			student.save()
			send_mail("Schedule Changes to review", "Hello; your parent has some suggestions for you: " +message, '', [student.email])
		else: 
			return HttpResponse("Student hasn't submitted")
	return HttpResponse("Message sent to %s %s successfully" %(student.first_name, student.last_name))

def ParentConfirm(request, Activation_key):
	student = get_object_or_404(Student, activation_key=Activation_key)
	studentHouseParent = StudentHouseParent.objects.get(studentIDNumber = student.id)
	parents, parentEmails = parentNamesandEmails(studentHouseParent)
	return render_to_response('registrationApp/ParentConfirm.html', {'student':student, 'parents': parents},
								context_instance=RequestContext(request))

def ParentConfirmYes(request):
	msg=""
	if request.is_ajax():
		stud = request.POST.get('student')
		student = get_object_or_404(Student, pk=stud)
		if student.submit:
			if student.parentApproval == True:
				msg= "You've already approved your child!"
			else:
				student.parentApproval = True
				student.save()
				msg="Thanks for your approval!"
				studentHouseParent = StudentHouseParent.objects.get(studentIDNumber = student.id)
	    		advisor, emails = advisorNamesandEmails(studentHouseParent)
	    		emails.append(student.email)
	    		send_mail("Parent Approval of Schedule", "Hello; your parent has approved your schedule! ", '', emails)
    	else:
	    	return HttpResponse("Student has not submitted")
	return HttpResponse(msg)
