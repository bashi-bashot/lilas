from django.db import models
from django.utils import timezone


class ConfigurationSalle(models.Model):
    date = models.DateTimeField()   #Il faudrait faire un test dans le programme pour savoir si la valeur par défaut a été utilisée
    
    class Meta:
        ordering = ['date']
    
    def __str__(self):
        # return self.date.__str__() # Pour test affichage "conf" dans chrgt_conf_salle
        return self.date.__str__()

        
        
class Uce(models.Model):
    configurationSalle = models.ForeignKey(ConfigurationSalle, related_name='confUce', on_delete=models.CASCADE)   # related_name (par défaut: uce_set) permet de définir le nom à
    nomUce = models.CharField(max_length=30)                                                                       # utiliser pour la relation inverse depuis l’objet lié vers celui-ci.
    secteurs = models.CharField(max_length=300)
    
    class Meta:
        ordering = ['configurationSalle']
    
    def __str__(self):
        return '%s: %s' % (self.nomUce, self.secteurs)

