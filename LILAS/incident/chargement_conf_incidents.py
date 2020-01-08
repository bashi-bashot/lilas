#Algorithme qui sert à trier les tickets de INCIDENTS
#Extraire les champs importants
#Utiliser les fonctionnalités Django pour créer la base de données

from incident.models import Incident
from django.conf import settings
from datetime import datetime
import pytz



def recupFichier():
    """
    Cette fonction récupère le fichier csv et renvoie un tableau à deux dimensions.
    La première correspond à un ticket et la deuxième correspond à chaque élément du ticket.
    """
    #On ouvre le fichier contenant els tickets
    fic = open("temp_media/tickets_incidents.csv", 'r')
    t = fic.readlines() #on stock dans t toutes les lignes du fichier de tickets --> Chaque ligne EST un ticket
    fic.close() #On ferme le flux
    
    u = [] #u est comme t, à la différence que chaque colonne est un champ du ticket
    
    for i in range(len(t)): #On parcourt tous les tickets ----- len(t)
        u.append(t[i].split(",")) #On sépare les champs du ticket et on enlève les guillemets
    return u
    
    
def traitementTicketIncident(tabIncidents):
    #On instancie un objet Incident de la forme : 
    
    #Incident(type_element, nom_element, etat_element, gravite, date_apparition, date_disparition_systeme)
    #Incident(          16,          17,           18,      27,              28,                       30)
    timzeone = pytz.timezone('UTC')
    for p in range(len(tabIncidents)): #Tant qu'il y a des tickets
        
        #On récupère la date au champ 23
        texteDate = tabIncidents[p][28][1:-1]
        texteDateFin = tabIncidents[p][30][1:-1]
            
        
        d = datetime(int(texteDate[27:29])+2000,int(texteDate[24:26]),int(texteDate[21:23]),int(texteDate[30:32]),int(texteDate[33:35]),int(texteDate[36:38]))   
        nom_element = tabIncidents[p][17][1:-1]
        
        if Incident.objects.filter(date_apparition__contains=d).filter(nom_element__contains=nom_element).count()==1:
            print(nom_element+" "+d.__str__()+" deja present")
            pass
        else:
            if(len(texteDateFin) == 22):
                dfin = datetime(int(texteDate[27:29])+2000,int(texteDate[24:26]),int(texteDate[21:23]),23,59,59) #Si la date de fin n'est pas renseignée, on prend le jour du début à 23h59m59s
            else :
                dfin = datetime(int(texteDateFin[28:30])+2000,int(texteDateFin[25:27]),int(texteDateFin[22:24]),int(texteDateFin[31:33]),int(texteDateFin[34:36]),int(texteDateFin[37:39]))
            
            i = Incident(type_element = tabIncidents[p][16][1:-1], nom_element = tabIncidents[p][17][1:-1], etat_element = tabIncidents[p][18][1:-1], gravite = tabIncidents[p][27][1:-1],date_apparition = d, date_disparition_systeme = dfin)
            i.save()
    
 
liste = recupFichier()
traitementTicketIncident(liste)

# Commande shell manage.py : exec(open('incident/chargement_conf_incidents.py').read())