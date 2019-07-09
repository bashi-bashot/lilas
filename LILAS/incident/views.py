from django.shortcuts import render
from django.http import HttpResponse
from incident.models import Incident
from django.template import loader
from django.views import generic
from .forms import DateForm




from datetime import datetime
import pytz

def index(request):
    
    # IncidentListe = Incident.objects.all() #On récupère la liste de tous les Incidents --> PEUT POSER PROBLEME SI ON EN A 150 000
    
    if request.method == 'POST': #Si on a rempli le formulaire /!\ Chercher comment différencier les différents formulaire d'une même page /!\
        form = DateForm(request.POST)
        IncidentListe = Incident.objects.all()
        # context = {'IncidentListe':IncidentListe, 'form':form} 
        if form.is_valid():
            dateDeb = form.cleaned_data['dateDebut'] #On récupère la dete de début entrée dans le formulaire
            dateF = form.cleaned_data['dateFin'] #On récupère la dete de fin entrée dans le formulaire
            
            strHeureDebut = form.cleaned_data['heureDebut'] #On récupère l'heure de début sous forme de chaine de caractère (pour le moment)
            strHeureFin = form.cleaned_data['heureFin'] #On récupère l'heure de fin sous forme de chaine de caractère (pour le moment)
            
            # print(strHeureDebut)
            
            #On crée ensuite les objets datetime de début et de fin
            date_time_deb = datetime( dateDeb.year, dateDeb.month, dateDeb.day, int(strHeureDebut[0:2]),int(strHeureDebut[3:5]), int(strHeureDebut[6:8])) #date naive
            date_time_fin = datetime( dateF.year, dateF.month, dateF.day, int(strHeureFin[0:2]), int(strHeureFin[3:5]), int(strHeureFin[6:8])) #date naive aussi
            
            timzeone = pytz.timezone('UTC') #Définition de la zone horaire pour rendre la date aware
            date_time_deb_aware = timzeone.localize(date_time_deb)
            date_time_fin_aware = timzeone.localize(date_time_fin)
            
            #On change la variable contexte à envoyer au html
            
            liste=[] #liste contient tous les tickets d'incidents de la période séléctionnée
            
            for i in IncidentListe :
                if i.date_apparition > date_time_deb_aware and i.date_disparition_systeme < date_time_fin_aware :
                    liste.append(i)
            
                
            
            #On génère le tableau de statistiques
            #On commence par recenser tous les éléments tombés en panne (On ne met qu'une seule fois les éléments rombé en panne plusieurs fois)
            
            listeElement=[] #Liste qui contient tous les éléments tombés en panne
            listeStats=[] #Liste où sont tockées les statistiqyes (nombre d'occurrence et durée d'indisponnibilité)
            
            
            
            for element in liste :
                if(element.nom_element not in listeElement):
                    listeElement.append(element.nom_element)
                    listeStats.append([element.nom_element])
                  
                #element.nom_element figure forcement dans listeStats et listeElement
                #On récupère l'indice de listeStats auquel on a ajouté l'élément
                indice = listeElement.index(element.nom_element)
                
                #On ajoute 3 zéros au tableau listeStats[indice]
                for i in range(2):
                    listeStats[indice].append(0)
                
                #On incrémente le nombre d'occurrence 
                listeStats[indice][1] = listeStats[indice][1] + 1
                
                #On ajoute la durée d'indisponnibilité
                d1 = element.date_apparition
                d2 = element.date_disparition_systeme
                dur = d2-d1
                listeStats[indice][2] = listeStats[indice][2] + int(dur.total_seconds())
                   
            
            
            context = {'IncidentListe':liste, 'form':form, 'listeStats':listeStats} 
        
    else:
        form = DateForm(request.POST)
        # context = {'IncidentListe':IncidentListe, 'form':form} 
        context = {'form':form}
        
    return render(request, 'incident/index.html', context)
    
    

    def get_queryset(self):
        return 0