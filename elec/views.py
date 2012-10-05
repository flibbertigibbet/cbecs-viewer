# Create your views here.
from django.http import HttpResponse

welcomepage = """<html>
<head>
<title>
Welcome to CBECS Viewer
</title>
<body bgcolor="#ddffdd">
<h1>howdy!</h1>
This will be the home page.
</body>
</html>
"""
from django.template import Context, RequestContext
from django.shortcuts import render_to_response

thecontext = Context({"pagetitle":"Howdy!",
                   "pagecontent":"This will be the home page."})

"""
def hello(request):
    return HttpResponse(welcomepage)
"""

from elec.models import Building, CensusDiv
from django.forms import ModelForm, ModelChoiceField, Form, Select, ChoiceField

class MyModelChoiceField(ModelChoiceField):
	def label_from_instance(self, obj):
		return obj[0]

# form class
class DemoForm(Form):
	CensusDiv = MyModelChoiceField(queryset=CensusDiv.objects.values_list('desc'), 
		empty_label=None, label="Census Division",required=False)

def dbdemo(request):
    b = Building.objects.get(pubid="1")
    dbcontext = Context({"pagetitle":"DB demo",
                       "pagecontent":"the area is %s sq ft" % b.area})
    return render_to_response("basic.html",dbcontext)

def hello(request):
    return render_to_response("basic.html",thecontext)

def formdemo(request):
	if request.method == 'POST':
		form = DemoForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/thanks/')
			
	else:
		form = DemoForm() # redirect after POST
	
	formcontext = Context({"pagetitle":"form demo",
                       "pagecontent":"Census Division"})		
	return render_to_response("formdemo.html",{'form':form,})
