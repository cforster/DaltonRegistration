from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from registrationApp.models import Student, Course, Section, Discipline
import re
import pprint

def index(request):
	studentInformation= Student.objects.all()[:5]
	output = ', '.join([p.firstName for p in studentInformation])
	return HttpResponse(output)

def detail(request):
	studentInformation= Student.objects.all()[:5]
	output = ', '.join([p.firstName for p in studentInformation])
	return HttpResponse(output)	

def search(request):
    return render_to_response('registrationApp/search.html',
							   context_instance=RequestContext(request))

def searchResults(request):
	courseOptions= Course.objects.filter(courseName__icontains=request.POST.get('search'))
	sectionOptions= Section.objects.filter(courseID=courseOptions)
	disciplineOptions= ([e.discipline for e in courseOptions])
	d=([d.discipline for d in disciplineOptions])
	results = ([c.courseName + '--' + c.courseDescription for c in courseOptions])
	sectionResults= ([s.APeriodDays + ' ' + s.BPeriodDays + ' ' + s.CPeriodDays + ' ' + s.DPeriodDays + ' ' + s.EPeriodDays + ' ' + s.FPeriodDays + ' ' + s.GPeriodDays + ' ' +  s.HPeriodDays + ' ' + s.IPeriodDays + ' ' + s.KPeriodDays + ' ' + s.ZPeriodDays for s in sectionOptions])
	output=[]
	for r, sr, discipline in map(None, results, sectionResults, d):
		output.append(str(r)+" "+str(sr)+ " "+str(discipline))
	return HttpResponse("<br>".join(output))