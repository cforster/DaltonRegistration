from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.db.models import Q
import re
from registrationApp.models import Student, Course, Section, Discipline, StudentSchedule

def index(request):
	studentInformation= Student.objects.all()[:5]
	output = ', '.join([p.firstName for p in studentInformation])
	return HttpResponse(output)

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
	#try:
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
		return render_to_response('registrationApp/searchResults.html', {'courseOptions' : courseOptions,'allSec' : allSec},
						context_instance=RequestContext(request))


							
def add(request, Student_id):
	u = get_object_or_404(Student, pk=Student_id)
	msg = ""
	section = ""
	if request.is_ajax():
		sec = request.GET.get('section')
		if sec:
			section = Section.objects.get(pk=sec)
			if section is not None:
				section, created= StudentSchedule.objects.get_or_create(
				studentID = u, sectionID=section,rank=1)
				if created == False:
					msg = "Could not add " +Section.objects.get(pk=sec).courseID.courseName + "; you are already enrolled"
				else:
					msg = "Course Created"
	studentSchedule = StudentSchedule.objects.filter(studentID = u)
	return render_to_response('registrationApp/add.html', {'student': u, 'studentSchedule': studentSchedule, 'section': section, 'msg' : msg},
							    context_instance=RequestContext(request))	
							 
def delete(request, Student_id):
	z = get_object_or_404(Student, pk=Student_id)
	if request.is_ajax():
		studSched = request.GET.get('studSched')
		studSchedObj = StudentSchedule.objects.get(pk = studSched)
		if studSchedObj is not None:
			studSchedObj.delete()
			msg = "Section Deleted"
			studentSchedule = StudentSchedule.objects.filter(studentID = z)
			return render_to_response('registrationApp/add.html', {'student': z, 'studentSchedule': studentSchedule, 'msg': msg},
							   			context_instance=RequestContext(request))	
		else: 
			return HttpResponse("Could not delete; obj does not exist")