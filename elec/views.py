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

from elec.models import Building, Regions, SqftCat, YearConstructed
from django.forms import ModelForm, ModelChoiceField, Form, Select, ChoiceField
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Count, Avg

class MyModelChoiceField(ModelChoiceField):
	def label_from_instance(self, obj):
		return obj[1]

# form class
class DemoForm(Form):
	Regions = MyModelChoiceField(queryset=Regions.objects.values_list(), 
		empty_label="All",required=False, label="Region")
	SqftCat = MyModelChoiceField(queryset=SqftCat.objects.values_list(), 
		empty_label="All",required=False, label="Square footage")
	YearConstructed = MyModelChoiceField(queryset=YearConstructed.objects.values_list(), 
		empty_label="All",required=False, label="Year Constructed")
	
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
		
		# get results
		# default to all
		b = Building.objects.all()
		c = Building.objects.count()
		avg = Building.objects.aggregate(myavg=Avg('tot_elec'))
		bldgtitle = "All buildings"
		sqfttitle = "All sizes"
		yrconsttitle = "All years"
		
		if len(request.POST.get('Regions')) > 0:
			myresponse = int(request.POST.get('Regions')[1])
			b = Building.objects.filter(region=myresponse)
			areaname = request.POST.get('Regions')[6:-2]
			bldgtitle = "Buildings in: " + areaname
			
		if len(request.POST.get('YearConstructed')) > 0:
			resp = int(request.POST.get('YearConstructed')[1])
			b = b.filter(yrcon=resp)
			yrconsttitle = "Year constructed: " + request.POST.get('YearConstructed')[6:-2]
			
		if len(request.POST.get('SqftCat')) > 0:
			resp = int(request.POST.get('SqftCat')[1])
			b = b.filter(area_cat=resp)
			sqfttitle = "Square footage: " + request.POST.get('SqftCat')[6:-2]
			
		c = b.count()
		avg = b.aggregate(myavg=Avg('tot_elec'))
		
		aContext = Context({"pagetitle":"Search CBECS", "bldgtitle":bldgtitle, \
			"buildings":b,"count_bldgs":c, "avg_cons":avg['myavg'], \
			"sqfttitle":sqfttitle,"yrconsttitle":yrconsttitle})
			
		return render_to_response("results_table.html", aContext)
	else:
		form = DemoForm() # redirect after POST
	
	formcontext = Context({"pagetitle":"form demo",
                       "pagecontent":"Census Division"})		
	return render_to_response("formdemo.html",{'form':form,}, \
		context_instance=RequestContext(request))
