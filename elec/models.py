from django.db import models

# Create your models here.

class CensusDiv(models.Model):
	desc = models.CharField(max_length=50)

class Building(models.Model):
    pubid = models.IntegerField() #PUBID8
    activity = models.IntegerField() #PBA8
    region = models.IntegerField() #REGION8
    #region = models.ForeignKey('CensusDiv')
    area = models.IntegerField() #SQFT8
    area_cat = models.IntegerField() #SQFTCX
    yrcon = models.IntegerField() #YEARCAT
    heat = models.IntegerField() #ELHTBTU8
    cooling = models.IntegerField()  #ELCLBTU8 
    ventilat = models.IntegerField()  #ELVNBTU8 
    waterheat = models.IntegerField()  #ELWTBTU8 
    lighting = models.IntegerField()  #ELLTBTU8 
    cooking = models.IntegerField()  #ELCKBTU8 
    refrig = models.IntegerField()  #ELRFBTU8 
    office = models.IntegerField()  #ELOFBTU8 
    computer = models.IntegerField()  #ELPCBTU8 
    misc = models.IntegerField()  #ELMSBTU8 


