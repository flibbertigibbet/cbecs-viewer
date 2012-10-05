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

from elec.models import Building, Region
from django.forms import ModelForm, ModelChoiceField, Form, Select, ChoiceField
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Count, Avg

class MyModelChoiceField(ModelChoiceField):
	def label_from_instance(self, obj):
		return obj[1]

# form class
class DemoForm(Form):
	Region = MyModelChoiceField(queryset=Region.objects.values_list(), 
		empty_label="All",required=False)

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
		
		# get result
		if len(request.POST.get('Region')) > 0:
			myresponse = int(request.POST.get('Region')[1])
			b = Building.objects.filter(region=myresponse)
			areaname = request.POST.get('Region')[6:-2]
			bldgtitle = "buildings in " + areaname
			q = Building.objects.filter(region=myresponse)
			c = q.count()
			avg = q.aggregate(myavg=Avg('tot_elec'))
		
			aContext = Context({"pagetitle":bldgtitle, \
				"buildings":q,"count_bldgs":c, "avg_cons":avg['myavg']})
		else:
			c = Building.objects.count()
			avg = Building.objects.aggregate(myavg=Avg('tot_elec'))
			bldgtitle = "All buildings"
			
		aContext = Context({"pagetitle":bldgtitle, \
			"buildings":Building.objects.all(),"count_bldgs":c, "avg_cons":avg['myavg']})
			
		return render_to_response("results_table.html", aContext)
	else:
		form = DemoForm() # redirect after POST
	
	formcontext = Context({"pagetitle":"form demo",
                       "pagecontent":"Census Division"})		
	return render_to_response("formdemo.html",{'form':form,}, \
		context_instance=RequestContext(request))
