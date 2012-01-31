from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.db.models import Q
import re
from registrationApp.models import Student, Course, Section, Discipline, StudentSchedule,PreApproval
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def index(request):
	studentInformation= Student.objects.all()[:5]
	output = ', '.join([p.firstName for p in studentInformation])
	return HttpResponse(output)

@login_required(login_url='/login/')
def search(request, Student_id):
	s = get_object_or_404(Student, pk=Student_id)
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

def searchResults(request, Student_id):
	t = get_object_or_404(Student, pk=Student_id)
	if request.is_ajax():
		searchTerms = request.GET.get('q')
		searchTerms = searchTerms.replace("_", " ")
		allSec = []
		found = get_query((searchTerms), ['courseName', 'courseDescription', 'discipline__discipline'])
        if found is not None:            
        	courseOptions = Course.objects.filter(found)
        	for course in courseOptions:
	        	courseSelected = Course.objects.get(pk=course.id)
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
								
def ApprovalMethod(courseID):
	preApproved = False
	preApprovals = PreApproval.objects.filter(courseID = courseID)
	for preApp in preApprovals:
		if preApp.courseID == courseID:
			preApproved = True
		if preApproved == False: 
			msg = "You are not preapproved for " + courseID.courseName
	return(preApproved)

def add(request, Student_id):
	u = get_object_or_404(Student, pk=Student_id)
	msg = ""
	section = ""
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
						preApproved =ApprovalMethod(section.courseID)
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
								output.append("you're enrolled")
								continues = False
						if continues != False:
							for studSched in studentSchedule:
								if studSched.sectionID.courseID == Section.objects.get(pk=sec).courseID:
									alreadyEnrolled = True
									msg = "You are already enrolled in a section of " + Section.objects.get(pk=sec).courseID.courseName + "Are you sure you want to add it? "
						if alreadyEnrolled != True:
							section, created= StudentSchedule.objects.get_or_create(
							studentID = u, sectionID=section,rank=1)
							if created == False:
								msg = "Could not add " + Section.objects.get(pk=sec).courseID.courseName +  " " + str(section) + "; you are already enrolled"
							else: 
								msg = Section.objects.get(pk=sec).courseID.courseName+ " Added "
				else:
					msg = section.courseID.courseName + " is not offered for " + str(u.grade) + " grade"				

		studentSchedule = StudentSchedule.objects.filter(studentID = u)
		secOption = periodSwitch(studentSchedule)
		return render_to_response('registrationApp/add.html', {'student': u, 'studentSchedule': studentSchedule, 'section': section, 'msg' : msg, 'secOption' : secOption},
								    context_instance=RequestContext(request))			

						

def addEnrolledSection(request, Student_id):
	stud = get_object_or_404(Student, pk=Student_id)
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
				msg = Section.objects.get(pk=sec).courseID.courseName+ " Added. Please ensure you are not in two sections "
	studentSchedule = StudentSchedule.objects.filter(studentID = stud)
	secOption = periodSwitch(studentSchedule)				
	return render_to_response('registrationApp/add.html', {'student': stud, 'studentSchedule': studentSchedule, 'section': section, 'msg' : msg, 'secOption' : secOption},
								    context_instance=RequestContext(request))	
							 
def delete(request, Student_id):
	z = get_object_or_404(Student, pk=Student_id)
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

def one(request, Student_id):
	a = get_object_or_404(Student, pk=Student_id)
	courses = Course.objects.all()
	name = []
	desc = []
	for c in courses:
		name.append(c.courseName)
		name.append("<br><br>")
		desc.append(c.courseDescription)
		

	return HttpResponse(name)

