from django.db import models

# Create your models here.

class Incident(models.Model):
    type_element = models.CharField(max_length=30) 
    nom_element = models.CharField(max_length=30) 
    etat_element = models.CharField(max_length=30) 
    gravite = models.CharField(max_length=30) 
    date_apparition = models.DateTimeField() 
    date_disparition_systeme = models.DateTimeField() 
    
    def __str__(self):
        return self.type_element+","+self.nom_element+","+self.etat_element+","+str(self.date_apparition)
