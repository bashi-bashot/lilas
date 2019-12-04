from django.db import models
    

class Date(models.Model):
    date = models.DateField() 

    def __str__(self):
        return self.date.__str__()

class Appel(models.Model):
    appelant = models.CharField(max_length=30) 
    appele = models.CharField(max_length=30)
    date = models.ForeignKey(Date, related_name='Appel', on_delete=models.CASCADE) 
    heure = models.TimeField()
    type = models.CharField(max_length=30)
    duree =models.IntegerField()
    liberation = models.CharField(max_length=30)
    line_appelante = models.CharField(max_length=30, default='xxxxx')
    line_appele = models.CharField(max_length=30, default='xxxxx')
    etat = models.CharField(max_length=30, default='xxxxx') #Peut être 'ETABLI',  'ECHEC' ou 'REFUS'
    fx_entrant = models.CharField(max_length=30, default='fx_xxxx_e')
    fx_sortant = models.CharField(max_length=30, default='fx_xxxx_s')
    nom_appele = models.CharField(max_length=30, default='non renseigne')
    nom_appelant = models.CharField(max_length=30, default='non renseigne')
    SUTP = models.BooleanField(default = False)
    SDA =  models.BooleanField(default = False)
    
    
    
    def __str__(self):
        return self.appelant+", "+self.appele+", "+self.date.__str__()+", "+self.type+", "+str(self.duree)+"s"+","+str(self.SUTP)
    

class NumExterieur(models.Model):
    id_elts = models.CharField(max_length=4) #Maximum 99 999 numéros
    id_lilas = models.CharField(max_length=4) #Maximum 99 999 numéros
    numero = models.CharField(max_length=15)
    nom = models.CharField(max_length=30)
    
    class Meta:
        ordering = ['nom']
    
    def __str__(self):
        return self.nom+", "+self.numero
        
class Faisceau(models.Model):
    id_elts = models.CharField(max_length=4) #Maximum 9999 numéros
    id_lilas = models.CharField(max_length=4) #Maximum 9999 numéros
    nom = models.CharField(max_length=30)
    
    def __str__(self):
        return self.nom+", "+self.id_elts+", "+self.id_lilas
        
    class Meta :
        verbose_name_plural = "Faisceaux"
    
class LIF(models.Model):
    id_elts = models.CharField(max_length=4)
    id_lilas = models.CharField(max_length=4)
    faisceau = models.ForeignKey(Faisceau, on_delete=models.CASCADE)
    nom = models.CharField(max_length=30)
    
    class Meta:
        ordering = ['nom']
    
    def __str__(self):
        return "LIF : "+self.nom+", Faisceau : "+self.faisceau.nom+", ID_ELTS : "+self.id_elts
    
    
class NumSecteur(models.Model):
    id_elts = models.CharField(max_length=4) #Maximum 9999 numéros
    id_lilas = models.CharField(max_length=4) #Maximum 9999 numéros
    numero = models.CharField(max_length=15)
    nom = models.CharField(max_length=30)
    
    def __str__(self):
        return self.nom+", "+self.numero