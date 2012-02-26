from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.db.models import Q
from registrationApp.models import Student, Course, Section, Discipline, StudentSchedule,PreApproval, DepartmentChair, House, ParentStudent
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.mail import send_mail
import re, datetime, random, sha

def index(request):
	studentInformation= Student.objects.all()[:5]
	output = ', '.join([p.firstName for p in studentInformation])
	return HttpResponse(output)

@login_required(login_url='/registrationApp/login/')
def search(request):
	s = get_object_or_404(Student, user=request.user.id)
	return render_to_response('registrationApp/search.html', {'student': s},
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

@login_required(login_url='/registrationApp/login/')
def searchResults(request):
	t = get_object_or_404(Student, user=request.user.id)
	if request.is_ajax():
		searchTerms = request.GET.get('q')
		searchTerms = searchTerms.replace("_", " ")
		allSec = []
		courseOptions = []
		found = get_query((searchTerms), ['courseName', 'courseDescription', 'discipline__discipline'])
        if found is not None:
        	courseOptions = Course.objects.filter(found)
        	for course in courseOptions:
	        	courseSelected = Course.objects.get(pk = course.id)
	        	sectionOptions = Section.objects.filter(courseID = courseSelected)
	        	sections = []
	        	for s in sectionOptions:
		        	sections.append(s)
		        allSec.append(sections)
		return render_to_response('registrationApp/searchResults.html', {'student': t, 'courseOptions' : courseOptions,'allSec' : allSec},
						context_instance=RequestContext(request))

def daysToPeriod(s):
	output = []
	if not "0" in s.APeriodDays:
		output.append("A")
	if not "0" in s.BPeriodDays:
		output.append("B")
	if not "0" in s.CPeriodDays:
		output.append("C")
	if not "0" in s.DPeriodDays:
		output.append("D")
	if not "0" in s.EPeriodDays:
		output.append("E")
	if not "0" in s.FPeriodDays:
		output.append("F")
	if not "0" in s.GPeriodDays:
		output.append("G")
	if not "0" in s.HPeriodDays:
		output.append("H")
	if not "0" in s.IPeriodDays:
		output.append("I")
	if not "0" in s.KPeriodDays:
		output.append("K")
	if not "0" in s.ZPeriodDays:
		output.append("Z")		
	return output

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

def ApprovalMethod(courseID, student):
	preApproved = False
	preApprovals = PreApproval.objects.filter(studentID = student)
	for preApp in preApprovals:
		if preApp.courseID == courseID:
			preApproved = True
		if preApproved == False: 
			msg = "You are not preapproved for " + courseID.courseName
	return(preApproved)
#remove avail for grade
#searchrank 
#parent/login
#unsubmit/reject 
#

@login_required(login_url='/registrationApp/login/')
def add(request):
	student = request.GET.get('student')
	if student is not None:
		u = get_object_or_404(Student, user = student)
	else:
		u = get_object_or_404(Student, user=request.user.id)
	msg = ""
	section = ""
	if u.submit:
		msg = "You've already submitted!"
	if request.is_ajax():
		sec = request.GET.get('section')
		if sec:
			section = Section.objects.get(pk=sec)
			if section is not None:
				continues = True
				availForGrade = False
				alreadyEnrolled = False
				sectionGradesOffered = str(section.courseID.grades_Offered)
				lis = [x.strip() for x in sectionGradesOffered .split(',')]
				for l in lis:
					if u.grade == int(l):
						availForGrade = True
				if availForGrade == True:
					if section.courseID.preapprovalRequired == True:
						preApproved =ApprovalMethod(section.courseID, u.id)
						if preApproved == False: 
							msg = "You are not preapproved for " + section.courseID.courseName
							continues = False
						elif preApproved == True:
							continues = True
					if continues == True:
						studentSchedule = StudentSchedule.objects.filter(studentID = u)
						output = []
						for studSched in studentSchedule:
							if studSched.sectionID == Section.objects.get(pk=sec):
								continues = False
						if continues != False:
							for studSched in studentSchedule:
								if studSched.sectionID.courseID == Section.objects.get(pk=sec).courseID:
									alreadyEnrolled = True
									msg = "You are already enrolled in a section " + str(section) + " of " + Section.objects.get(pk=sec).courseID.courseName + " Are you sure you want to add it? "
						if alreadyEnrolled != True:
							#cycle through periods to see if there is any conflict
							section, created= StudentSchedule.objects.get_or_create(
							studentID = u, sectionID=section,rank=1)
							if created == False:
								msg = "Could not add " + Section.objects.get(pk=sec).courseID.courseName +  " " + str(section) + "; you are already enrolled"
							else: 
								msg = Section.objects.get(pk=sec).courseID.courseName+ " Added "
				else:
					msg = section.courseID.courseName + " is not offered for " + str(u.grade) + " grade"				
	fromOther = request.GET.get('fromOther')
	if fromOther is not None:
		if int(fromOther) == 1:
			msg=""
	studentSchedule = StudentSchedule.objects.filter(studentID = u)
	secOption = periodSwitch(studentSchedule)
	return render_to_response('registrationApp/add.html', {'student': u, 'studentSchedule': studentSchedule, 'section': section, 'msg' : msg, 'secOption' : secOption},
								context_instance=RequestContext(request))			

						
@login_required(login_url='/registrationApp/login/')
def addEnrolledSection(request):
	stud = get_object_or_404(Student, user=request.user.id)
	msg = ""
	if request.is_ajax():
		sec = request.GET.get('section')
		if sec:
			section = Section.objects.get(pk=sec)
			section, created= StudentSchedule.objects.get_or_create(
			studentID = stud, sectionID=section,rank=1)
			if created == False:
				msg = "Could not add " + Section.objects.get(pk=sec).courseID.courseName +  " " + str(section) + "; you are already enrolled"
			else: 
				msg = Section.objects.get(pk=sec).courseID.courseName+ " Added. Please ensure you are intentionally in two sections "
	studentSchedule = StudentSchedule.objects.filter(studentID = stud)
	secOption = periodSwitch(studentSchedule)				
	return render_to_response('registrationApp/add.html', {'student': stud, 'studentSchedule': studentSchedule, 'section': section, 'msg' : msg, 'secOption' : secOption},
								    context_instance=RequestContext(request))	

@login_required(login_url='/registrationApp/login/')							 
def delete(request):
	z = get_object_or_404(Student, user=request.user.id)
	if request.is_ajax():
		studSched = request.GET.get('studSched')
		studSchedObj = StudentSchedule.objects.get(pk = studSched)

		if studSchedObj is not None:
			studSchedObj.delete()
			msg = studSchedObj.sectionID.courseID.courseName + " Deleted"
			studentSchedule = StudentSchedule.objects.filter(studentID = z)
			secOption = periodSwitch(studentSchedule)
			return render_to_response('registrationApp/add.html', {'student': z, 'studentSchedule': studentSchedule, 'msg': msg,'secOption' : secOption},
							   			context_instance=RequestContext(request))	
		else: 
			return HttpResponse("Could not delete; obj does not exist")

@login_required(login_url='/registrationApp/login/')
def one(request):
	a = get_object_or_404(Student, user=request.user.id)
	courses = Course.objects.all()
	name = []
	desc = []
	for c in courses:
		name.append(c.courseName)
		name.append("<br><br><br><br><br><br><br><br>")
		desc.append(c.courseDescription)
	return render_to_response('registrationApp/courseCatalog.html', {'student': a, 'courses' :courses})

@login_required(login_url='/registrationApp/login/')
def schedule(request):
	student = get_object_or_404(Student, user=request.user.id)
	studSched = StudentSchedule.objects.filter(studentID = student.id)
	courseName = []
	sectionID = []
	for section in studSched:
		courseName.append(section.sectionID.courseID)
		sectionID.append(section.sectionID)
		
#ical output
	#for sec in sectionID:
		#if str(sec.APeriodDays).contains('`1'):
			#sectionID.append("meets on monday!")  
	return HttpResponse(sectionID)
#col for sec; period; time


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
		send_mail("Schedule Changes to review", "Hello; your house advisor has some suggestions for you: " +message, 'darshandesai17@gmail.com', [student.email])
	return HttpResponse("Message sent to student successfully")

@login_required(login_url='/registrationApp/login/')
def submit(request):	
	student = get_object_or_404(Student, user=request.user.id)
	msg=""
	if student.submit == True:
		msg = "You have already submitted, please unsubmit first."
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