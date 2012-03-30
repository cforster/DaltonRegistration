from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.db.models import Q
from registrationApp.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from operator import itemgetter
import re, datetime, random, sha

def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)

def requiredCheck(student):
	studentSchedule = StudentSchedule.objects.filter(studentID = student)
	required = RequiredObjects.objects.filter(grade = student.graduationYear-2000)
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
	days = []
	sectionPeriods = section.__dict__
	for period, day in sorted(sectionPeriods.iteritems()):
		if "PeriodDays" in period and day:
			days.append(day)
			pAndD.append((period[0],day))

	pAndD.sort(key=itemgetter(1), reverse= True)
	for p, d in pAndD:
		periods += p
	return periods, days

def numbersToDay(numbers):
	output = ""
	for num in sorted(numbers):
		lists = [x.strip() for x in num.split(',')]
		for day in lists:
			if int(day) == 1:
				output += "Monday, "
			if int(day) == 2:
				output += "Tuesday, "
			if int(day) == 3:
				output += "Wednesday, "
			if int(day) == 4:
				output += "Thursday, "
			if int(day) == 5:
				output += "Friday One, "
			if int(day) == 6:
				output += "Friday Two, "
			if int(day) == 7:
				output += "Friday Three, "
			if int(day) == 8:
				output += "Friday Four, "
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

def sectionConflictPeriodCheck (student, course= None, section=None):
	msg = ""
	add =  False
	sec = ""
	studentSchedule = StudentSchedule.objects.filter(studentID = student)
	
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
		if student.graduationYear-2000 == int(l):
			availForGrade = True
		else:
			availForGrade = False	
	return availForGrade

def preApprovalCheck(student, course):
	preApprovals = PreApproval.objects.filter(studentID = student.id)
	preApproved = False
	for preApp in preApprovals:
		if preApp.courseID == course:
			preApproved = True
	return preApproved

def alreadyEnrolledCourse(student, course):
	alreadyEnrolledCourse = False
	sectionEnrolled = []
	studentSections = StudentSchedule.objects.filter(studentID = student.id)
	for studSched in studentSections:
		if studSched.sectionID.courseID == course:
			alreadyEnrolledCourse = True
			sectionEnrolled.append(studSched.sectionID)
	return alreadyEnrolledCourse, sectionEnrolled



@login_required
@group_required('student')
def searchResults(request):
#, 'discipline__discipline'
	t = get_object_or_404(Student, id=request.user.id)
	if request.is_ajax():
		searchTerms = request.POST.get('q')
		fromBox = request.POST.get('fromBox')
		courseOptions = []
		rank = []
		courseList = []                                        
		preApproved = True

        
		found = get_query((searchTerms), ['courseName', 'courseDescription', 'coursediscipline__discipline__discipline'])

        if found is not None:
        	if fromBox == "False":
        		courseOptions = Course.objects.filter(courseName__iregex=r'^%s.*'%searchTerms)
        	else:
        		courseOptions = Course.objects.filter(found).distinct()

        	for course in courseOptions:
				discipline = CourseDiscipline.objects.filter(courseID = course)
				rankScore = 0
				if str(course.courseName).lower() in searchTerms.lower():
					rankScore +=100
				for disc in discipline:
					if str(disc).lower() in searchTerms.lower():
						rankScore += 100
				availForGrade = gradeCheck(t, course)
				if availForGrade:
					rankScore += 10
				else:
					rankScore -= 30

				if course.preapprovalRequired:
					preApproved = preApprovalCheck(t, course)
					if preApproved:
						rankScore += 10
					else:
						rankScore -= 30
				alreadyEnrolledinCourse, sectionEnrolled = alreadyEnrolledCourse(t, course)
				if alreadyEnrolledinCourse:
					rankScore -= 20 

				requiredBoolList = requiredCheck(t)
				for req, reqPass in requiredBoolList:
					if not reqPass:
						if course == req.courseID:
							rankScore += 20
						else:
							for disc in discipline:
								if disc.discipline == req.discipline:
									rankScore += 20

				sectionOptions = Section.objects.filter(courseID = course.courseNumber)
				sections = []
				for section in sectionOptions:
					period, day = daysToPeriod(section)
					sections.append((section, period))

				courseList.append((course, rankScore, sections, availForGrade, preApproved, discipline))

				courseList.sort(key=itemgetter(1), reverse = True)
		if fromBox == "False":
			if courseList:
				return HttpResponse(courseList[0][0].courseName)
		else:
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
	
#remove avail for grade
#searchrank 
#parent/login
#unsubmit/reject 

# if submitted, reload same schedule: you can't submit
# otherwise get section, rank, discipline
# check if section is preapproved; if not, "you cannot add"
# check if section is already enrolled; if so, you cannot add
# check if course is already enrolled; if so redirect to yes/no
# check if grade available; if so redirect to yes no
# add course
# check for required courses, append to required list if not added by end

def studentScheduleAddView(studentSchedule):
	engHistRank = []
	engRank = []
	studSched = []
	same = False
	for sectionList in studentSchedule:
		discipline = CourseDiscipline.objects.filter(courseID = sectionList.sectionID.courseID.courseNumber)
		prd, dayz = daysToPeriod(sectionList.sectionID)
		if sectionList.sectionID.courseID.rankType == "EngHist":
			engHistRank.append((sectionList.sectionID.courseID, sectionList.rank))
		elif sectionList.sectionID.courseID.rankType == "English":
			engRank.append((sectionList.sectionID.courseID, sectionList.rank))

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
		studSched.append((sectionList, prd, discipline, sectionsOptions, engHistRank, engRank, dayz))
		studSched.sort(key=itemgetter(1))

	return studSched

def addSection(student, section, rank):
	studSchedule, created= StudentSchedule.objects.get_or_create(
						studentID = student, sectionID=section, rank=rank)
	if created:
		period, days = daysToPeriod(studSchedule.sectionID)
		msg = studSchedule.sectionID.courseID.courseName +" " + period + " Period Added "
	else: 
		msg = "Could not add "
	return msg

@login_required
@group_required('student')
def add(request):
	student = request.GET.get('student')
	if student is not None:
		u = get_object_or_404(Student, id = student)
	else:
		u = get_object_or_404(Student, id=request.user.id)
	section = ""
	confirmationBox = []
	rank = 0
	msg = []
	if u.submit:
		msg = "You've already submitted!"
	if request.is_ajax():
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
				add, sectionAdd, message, sect = sectionConflictPeriodCheck(u, course = courseObj)

				if add:
					msg.append(addSection(u, sectionAdd, 1))

				elif not add and confirm ==1:
					msg.append(addSection(u, sect, 1))

				elif not add:
					confirmationBox = [[True, courseObj]]
					msg.append(message)

		if sec:
			section = Section.objects.get(pk=sec)
			continues = True

			if section is not None:

				alreadyEnrolled = alreadyEnrolledSection(u, section)
				if alreadyEnrolled:
					period, days = daysToPeriod(section)
					msg.append("You are already enrolled in section " + period + " of " + section.courseID.courseName +".")
					continues = False

				elif section.courseID.preapprovalRequired:
					preApproved = preApprovalCheck(u, section.courseID)
					if not preApproved:
						msg.append("You are not preapproved for " + str(section.courseID.courseName) +".")
						continues = False

				if continues:
					
					availForGrade = gradeCheck(u, section.courseID)
				
					if availForGrade or (not availForGrade and confirm == 1):
						continues = True

					elif not availForGrade and confirm ==0:
						msg.append(section.courseID.courseName +" is not available for your grade. ")
						confirmationBox = [[True, ""]]
						continues = False
					
					alreadyEnrolledC, sectionEnrolled = alreadyEnrolledCourse(u, section.courseID)

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
					
					
					add, sectionAdd, mess, sect = sectionConflictPeriodCheck(u, section = section)

					if add and continues:
						msg.append(addSection(u, sectionAdd, 1))

					elif continues and not add and confirm ==1: 	
						msg.append(addSection(u, section, 1))

					elif not add:
						confirmationBox = [[True, ""]]
						msg.append(mess)
	
	fromOtherBool = False		
	fromOther = request.GET.get('fromOther')
	if fromOther is not None:
		if int(fromOther) == 1:
			fromOtherBool = True

	studentSchedule = StudentSchedule.objects.filter(studentID = u)

	requiredBoolList = requiredCheck(u)
	reqMessage = []
	for req, reqPass in requiredBoolList:
		if not reqPass:
			reqMessage.append((req, req.message))


	studentSchedules = studentScheduleAddView(studentSchedule)
	return render_to_response('registrationApp/add.html', {'student': u, 'studentSchedules': studentSchedules, 'section': section, 'msg' : msg, 'fromOtherBool' : fromOtherBool, 'reqMessage' : reqMessage, 'confirmationBox': confirmationBox},
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

@login_required
@group_required('student')						 
def delete(request):
	rank = 0 
	msg= []
	z = get_object_or_404(Student, id=request.user.id)
	if request.is_ajax():
		studSched = request.POST.get('studSched')
		studSchedObj = StudentSchedule.objects.get(pk = studSched)

		if studSchedObj is not None:
			if studSchedObj.sectionID.courseID.rankType:
				rank = studSchedObj.rank
			studSchedObj.delete()
			msg.append(studSchedObj.sectionID.courseID.courseName + " Deleted")
			studentSchedule = StudentSchedule.objects.filter(studentID = z)
			secOption = periodSwitch(studentSchedule)
			fromOtherBool = False
			requiredBoolList = requiredCheck(z)
			reqMessage = []
			for req, reqPass in requiredBoolList:
				if not reqPass:
					reqMessage.append((req, req.message))
			studentSchedules = studentScheduleAddView(studentSchedule)

			return render_to_response('registrationApp/add.html', {'student': z, 'studentSchedules': studentSchedules, 'msg': msg, 'fromOtherBool' : fromOtherBool,'reqMessage' : reqMessage},
							   			context_instance=RequestContext(request))	
		else: 
			return HttpResponse("Could not delete; section does not exist")

@login_required
@group_required('student')
def notifications(request):
	student = get_object_or_404(Student, id=request.user.id)
	if request.is_ajax():
		full = False
	else:
		full = True
	return render_to_response('registrationApp/notifications.html',{'student': student, 'full': full},
								context_instance=RequestContext(request))


@login_required
@group_required('student')
def notifRead(request):
	stud = get_object_or_404(Student, id=request.user.id)
	if request.is_ajax():
		notes = request.POST.get('note')
		notes = notes.split(",")
		for note in notes:
			if note == "advisor1Note":
				stud.advisor1NoteRead = 1
				stud.save()
			if note == "advisor2Note":
				stud.advisor2NoteRead = 1
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
	studentSchedule = StudentSchedule.objects.filter(studentID = student)

	requiredBoolList = requiredCheck(student)
	requiredList = []
	for req, reqPass in requiredBoolList:
		requiredList.append((req, reqPass, req.message))
	sections = studentScheduleAddView(studentSchedule)
	return render_to_response('registrationApp/one.html', {'student': student, 'sections'  : sections, 'requiredList': requiredList},
								context_instance=RequestContext(request))
@login_required
@group_required('student')
def rankChange(request):
	student = get_object_or_404(Student, id=request.user.id)
	if request.is_ajax():
		json_data = simplejson.loads(request.raw_post_data)
    	try:
      		data = json_data['data']
      		return HttpResponse(data)

    	except KeyError:
      		HttpResponseServerError("bad data")

		'''
		rankOrder= request.POST.get('rankOrder')
		ranks = rankOrder.split("&")
		for rank in ranks:
			return HttpResponse(ranks)
		return HttpResponse (ranks)
		'''
	'''
	msg = ""
	section = ""
	confirmationBox = False
	rank = 0
		studSched = request.GET.get('studSched')
		studSchedObj = StudentSchedule.objects.get(pk = studSched)
		oldRank = studSchedObj.rank

		newRank = request.GET.get('rank')
		oldRankObjects = StudentSchedule.objects.filter(rank = newRank)
		for oldRankObject in oldRankObjects:
			if oldRankObject.sectionID.courseID.rankType:
				oldRankObject.rank = oldRank
				oldRankObject.save()
		studSchedObj.rank = newRank
		studSchedObj.save()
		msg = studSchedObj.sectionID.courseID.courseName + "changed to rank " + studSchedObj.rank
	fromOtherBool = False		
	
	studentSchedule = StudentSchedule.objects.filter(studentID = student)

	requiredBoolList = requiredCheck(student)
	reqMessage = []
	for req, reqPass in requiredBoolList:
		if not reqPass:
			reqMessage.append((req, req.message))


	studSched = studentScheduleAddView(studentSchedule)
	return render_to_response('registrationApp/add.html', {'student': student, 'studSched': studSched, 'section': section, 'msg' : msg, 'fromOtherBool' : fromOtherBool, 'reqMessage' : reqMessage, 'confirmationBox': confirmationBox},
								context_instance=RequestContext(request))		
'''
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
		
	
#for sec in sectionID:
		#if str(sec.APeriodDays).contains('`1'):
			#sectionID.append("meets on monday!") 
#col for sec; period; time

@login_required(login_url='/registrationApp/login/')
def submit(request):	
	student = get_object_or_404(Student, id=request.user.id)
	msg=""
	if student.submit == True:
		msg = "You have already submitted!"
	else:
		student.submit = True
		student.save()
		salt = sha.new(str(random.random())).hexdigest()[:5]
    	activation_key = sha.new(salt+student.firstName).hexdigest()
    	student.activation_key = activation_key
    	student.save()
    	email_body = "http://127.0.0.1:8000/registrationApp/ParentConfirm/%s" % (student.activation_key)
    	send_mail("Your child has submitted their schedule",
          	  email_body,
              'darshandesai17@gmail.com',
              ["c12dd@dalton.org"])
    	msg = "Submitted for House Advisor and Parent Approval"
	return HttpResponse(msg)


def preapprovals(request, DepartmentChair_id):
	departmentChair = get_object_or_404(DepartmentChair, pk=DepartmentChair_id)
	disc = Discipline.objects.filter(departmentChair = departmentChair)
	for deparment in disc:
		courses = Course.objects.filter(discipline = deparment, preapprovalRequired = True)
	return render_to_response('registrationApp/preapprovals.html', {'departmentChair': departmentChair, 'courses': courses},
								context_instance=RequestContext(request))

def preAppContainer(request, DepartmentChair_id):
	departmentChair = get_object_or_404(DepartmentChair, pk=DepartmentChair_id)
	if request.is_ajax():
		courseID = request.GET.get('courseID')
		courseObj = Course.objects.get(pk = courseID)
	return render_to_response('registrationApp/preAppContainer.html', {'departmentChair': departmentChair, 'courseObj': courseObj},
								context_instance=RequestContext(request))

def preAppAdd(request, DepartmentChair_id):
	departmentChair = get_object_or_404(DepartmentChair, pk=DepartmentChair_id)
	msg = ""
	allCreated = True
	if request.is_ajax():
		courseID = request.GET.get('courseID')
		courseObj = Course.objects.get(pk = courseID)
		preAppName = request.GET.get('preAppName')
		preAppNames = str(preAppName).split(',')
		for preAppN in preAppNames:
			preAppN = str(preAppN).strip('_')
			preAppSplitN = str(preAppN).split('_')
			student = Student.objects.get(firstName__iexact = str(preAppSplitN[0]), lastName__iexact = str(preAppSplitN[1]))
			preApp, created= PreApproval.objects.get_or_create(
			studentID = student, courseID=courseObj)
			subject = "You were preapproved for " + courseObj.courseName
			message = "Hello " + student.firstName + "; you were preapproved for " + courseObj.courseName + "."
			if created == True:
				msg += student.firstName + " preapproval added <br> "
				send_mail(subject, message, 'darshandesai17@gmail.com', [student.email])
			elif created == False:
				msg += student.firstName + " is already preapproved <br> "
				allCreated = False
		if allCreated == True:
			msg = "All Added Successfully"
	return HttpResponse(msg)

@group_required('advisor')
def advisor(request, House_id):
	house = get_object_or_404(House, pk=House_id)
	students = Student.objects.filter(houseID=house)
	submittedStudents = [] 
	for stud in students:
		if stud.submit:
			submittedStudents.append(stud)
	return render_to_response('registrationApp/advisor.html', {'house':house, 'submittedStudents': submittedStudents},
								context_instance=RequestContext(request))

def approve(request, House_id):
	house = get_object_or_404(House, pk=House_id)
	if request.is_ajax():
		student = request.GET.get('student')
		stud = Student.objects.get(pk = student)
		stud.advisorApproval = True
		stud.save()
	return HttpResponse(stud.firstName + " was approved")

def review(request, House_id):
	house = get_object_or_404(House, pk=House_id)
	if request.is_ajax():
		student = request.GET.get('student')
		student = Student.objects.get(pk = student)
		message = request.GET.get('message')
		message = message.replace('_'," ")
		student.submit = False
		if student.advisor1Note:
			note = message + " PREVIOUS NOTE: " + student.advisor1Note
		else:
			note = message
		student.advisor1Note = note
		student.save()
		send_mail("Schedule Changes to review", "Hello; your house advisor has some suggestions for you: " +message, 'darshandesai17@gmail.com', [student.email])
	return HttpResponse("Message sent to student successfully")


def ParentConfirm(request, Activation_key):
	student = get_object_or_404(Student, activation_key=Activation_key)
	return render_to_response('registrationApp/ParentConfirm.html', {'student':student},
								context_instance=RequestContext(request))
							
def ParentConfirmYes(request):
	msg=""
	if request.is_ajax():
		stud = request.GET.get('student')
		student = get_object_or_404(Student, pk=stud)
		if student.parentApproval == True:
			msg= "You've already approved your child!"
		else:
			student.parentApproval = True
			student.save()
			msg="Thanks for your approval!"
	return HttpResponse(msg)
