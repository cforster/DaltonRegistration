from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from registrationApp.models import Student, Course
import re

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
	results = ([c.courseName + '--' + c.courseDescription for c in courseOptions])
	return HttpResponse('<br> '.join(results))