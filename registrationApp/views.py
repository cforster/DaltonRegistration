from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from registrationApp.models import Student

def index(request):
	studentInformation= Student.objects.all()[:5]
	output = ', '.join([p.firstName for p in studentInformation])
	return HttpResponse(output)


def detail(request, student_id):
    return render_to_response('registrationApp/detail.html',"hi")

def search(request, student_id):
    return render_to_response(course)