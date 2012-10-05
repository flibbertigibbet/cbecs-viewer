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
import urllib2, json

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
		bldgtitle = "All regions"
		sqfttitle = "All sizes"
		yrconsttitle = "All years"
		
		myresponse = 0
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
		
		##################
		# get average price for selected region/year from EIA
		avg_price = 0
		if myresponse == 0:
			# US - all sectors
			f = urllib2.urlopen('http://api.eia.gov/series/data?api_key=53A7FFDB82A49269E07949D71A2FFAE7&series_id=ELEC.PRICE.US-ALL.A')
			o = json.loads(f.read())
			k =o['series_data'][0]['data']
			for i in k:
				if i[0] == '2003':
					avg_price = i[1]
					break
					
		elif myresponse == 1:	
			# Northeast - Middle Atlantic, New England
			# Middle Atlantic
			f = urllib2.urlopen('http://api.eia.gov/series/data?api_key=53A7FFDB82A49269E07949D71A2FFAE7&series_id=ELEC.PRICE.MAT-ALL.A')
			o = json.loads(f.read())
			k =o['series_data'][0]['data']
			for i in k:
				if i[0] == '2003':
					avg1 = i[1]
					break
			# New England
			f = urllib2.urlopen('http://api.eia.gov/series/data?api_key=53A7FFDB82A49269E07949D71A2FFAE7&series_id=ELEC.PRICE.NEW-ALL.A')
			o = json.loads(f.read())
			k =o['series_data'][0]['data']
			for i in k:
				if i[0] == '2003':
					avg2 = i[1]
					break
			
			avg_price = (float(avg1) + float(avg2)) / 2.0
		
		elif myresponse == 2:
			# Midwest - East North Central and West North Central
			# EN Central
			f = urllib2.urlopen('http://api.eia.gov/series/data?api_key=53A7FFDB82A49269E07949D71A2FFAE7&series_id=ELEC.PRICE.ENC-ALL.A')
			o = json.loads(f.read())
			k =o['series_data'][0]['data']
			for i in k:
				if i[0] == '2003':
					avg1 = i[1]
					break
			
			# WN Central
			f = urllib2.urlopen('http://api.eia.gov/series/data?api_key=53A7FFDB82A49269E07949D71A2FFAE7&series_id=ELEC.PRICE.WNC-ALL.A')
			o = json.loads(f.read())
			k =o['series_data'][0]['data']
			for i in k:
				if i[0] == '2003':
					avg2 = i[1]
					break
				
			avg_price = (float(avg1) + float(avg2)) / 2.0
		
		elif myresponse == 3:
			# South - South Atlantic, East South Central, and West South Central
			# ES Central
			f = urllib2.urlopen('http://api.eia.gov/series/data?api_key=53A7FFDB82A49269E07949D71A2FFAE7&series_id=ELEC.PRICE.ESC-ALL.A')
			o = json.loads(f.read())
			k =o['series_data'][0]['data']
			for i in k:
				if i[0] == '2003':
					avg1 = i[1]
					break
					
			# S Atlantic
			f = urllib2.urlopen('http://api.eia.gov/series/data?api_key=53A7FFDB82A49269E07949D71A2FFAE7&series_id=ELEC.PRICE.SAT-ALL.A')
			o = json.loads(f.read())
			k =o['series_data'][0]['data']
			for i in k:
				if i[0] == '2003':
					avg2 = i[1]
					break
					
			# WS Central
			f = urllib2.urlopen('http://api.eia.gov/series/data?api_key=53A7FFDB82A49269E07949D71A2FFAE7&series_id=ELEC.PRICE.WSC-ALL.A')
			o = json.loads(f.read())
			k =o['series_data'][0]['data']
			for i in k:
				if i[0] == '2003':
					avg3 = i[1]
					break
			
			avg_price = (float(avg1) + float(avg2) + float(avg3)) / 3.0
			
		elif myresponse == 4:
			# West - Pacific and Mountain
			# Pacific contiguous
			f = urllib2.urlopen('http://api.eia.gov/series/data?api_key=53A7FFDB82A49269E07949D71A2FFAE7&series_id=ELEC.PRICE.PCC-ALL.A')
			o = json.loads(f.read())
			k =o['series_data'][0]['data']
			for i in k:
				if i[0] == '2003':
					avg1 = i[1]
					break
			
			# Pacific noncontiguous
			f = urllib2.urlopen('http://api.eia.gov/series/data?api_key=53A7FFDB82A49269E07949D71A2FFAE7&series_id=ELEC.PRICE.PCN-ALL.A')
			o = json.loads(f.read())
			k =o['series_data'][0]['data']
			for i in k:
				if i[0] == '2003':
					avg2 = i[1]
					break
			
			# Mountain
			f = urllib2.urlopen('http://api.eia.gov/series/data?api_key=53A7FFDB82A49269E07949D71A2FFAE7&series_id=ELEC.PRICE.MTN-ALL.A')
			o = json.loads(f.read())
			k =o['series_data'][0]['data']
			for i in k:
				if i[0] == '2003':
					avg3 = i[1]
					break
					
			avg_price = (float(avg1) + float(avg2) + float(avg3)) / 3.0
		#############
		
		if avg['myavg'] != None:
			avg_cons = round(float(avg['myavg']), 2)
		else:
			avg_cons = 0
		avg_price = round(float(avg_price), 2)
		
		aContext = Context({"pagetitle":"CBECS Results", "bldgtitle":bldgtitle, \
			"buildings":b,"count_bldgs":c, "avg_cons":avg_cons, \
			"sqfttitle":sqfttitle,"yrconsttitle":yrconsttitle,"avgprice":avg_price})
			
		return render_to_response("results_table.html", aContext)
	else:
		form = DemoForm() # redirect after POST
	
	formcontext = Context({"pagetitle":"form demo",
                       "pagecontent":"Census Division"})		
	return render_to_response("formdemo.html",{'form':form,}, \
		context_instance=RequestContext(request))
