from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from configSalle.models import Uce, ConfigurationSalle
from .forms import DateForm

# from django.core import serializers       # solution avortée du Json
# from configSalle.models import ConfSerializer
# import json

from datetime import datetime
import pytz

def index(request):
    # uceListe = Uce.objects.all() #On récupère la liste de toutes les conf des uce
    
    #LISTE DE VARIABLES GLOBALES
    formulaireDates = DateForm(request.POST)
    #---------------------------
    context = {'form':formulaireDates}
    
    if request.method == 'POST': #Si on a rempli un formulaire /!\ Chercher comment différencier les différents formulaire d'une même page /!\
            
            if formulaireDates.is_valid(): #Si on a rempli le formulaire de choix de date / secteur / correspondant pour afficher les appels
                # process the data in form.cleaned_data as required
                print("FORMULAIRE DATE VALIDE")
                uceListe = Uce.objects.all() #On récupère la liste de toutes les conf des uces
                confListe = ConfigurationSalle.objects.all() #On récupère la liste de toutes les configurationSalle effectuées
                
                date = formulaireDates.cleaned_data['date'] #On récupère la dete de début entrée dans le formulaire
                
                #On crée ensuite les objets datetime de début et de fin
                date_time_deb = datetime( date.year, date.month, date.day, 00, 00, 00) #date naive
                date_time_fin = datetime( date.year, date.month, date.day, 23, 59, 00) #date naive aussi
                
                timzeone = pytz.timezone('UTC') #Définition de la zone horaire pour rendre la date aware
                date_time_deb_aware = timzeone.localize(date_time_deb) #Pour faire le test suivant, le fuseau horaire de la date associée doit être renseigné 'aware'
                date_time_fin_aware = timzeone.localize(date_time_fin)
                
                
                #On change la variable contexte à envoyer au html
                #On crée la liste d'uces à afficher
                uces = []
                
                for i in uceListe :
                    if (i.configurationSalle.date > date_time_deb_aware) and (i.configurationSalle.date < date_time_fin_aware) : #Si la date de la conf sur l'uce est comprise entre les deux dates du formulaire
                            uces.append(i) #On ajoute l'uce à la fin de la liste
                
                
                #On crée la liste de confSalle à afficher
                confs = []
                dateSeconde = [] # Pour permettre un affichage des secondes < 10 sur 2 digits
                
                for i in confListe :
                    if (i.date > date_time_deb_aware) and (i.date < date_time_fin_aware) : #Si la date de la conf sur l'uce est comprise entre les deux dates du formulaire
                            confs.append(i) #On ajoute l'uce à la fin de la liste
                
                # data = serializers.serialize("json", uceListe)
                # with open("configSalle/data.json", 'a') as out:
                    # json.dump(data, indent=4, out)
                 
                # with open('configSalle/json/confs.json', 'w', encoding='utf-8') as f:
                    # f.write('[')
                    # for i in confs:
                        # # json.dump(i, f, indent=4, default=UceSerializer)
                        # confSerialize = ConfSerializer(i).data
                        # json.dump(confSerialize, f, indent=4)
                        # if confs.index(i) != len(confs)-1:
                            # f.write(',')
                    # f.write(']')
                    
                context = { 'uceListe':uces, 'confListe':confs, 'date':date, 'form':formulaireDates}
                
                # redirect to a new URL:
                return render(request, 'configSalle/index.html', context) #On recharge la pagee                
                
                
                
            #else :
                #Dans le cas où le formulaire n'est pas correct
                
                #Il faudrait ajouter un champ dans contexte qui contient une chaine de caractère du genre "Il est nécessaire de remplir tous les champs" 
                #puis de faire un test dans le html juste en dessous du formulaire tel que "Si ce champ de contexte existe, alors l'afficher,
                #sinon, ne pas l'afficher"
                
                #A ce moment là on a plus besoin de contexte juste avant "if form.is_valid():"

                #render(request, 'incident/index.html') #provisoire
                
    
    else :                  #Dans le cas où on a pas récupéré un POST 
        form = DateForm()   #On crée le formulaire à afficher
        bool = True         #Permet de différencier le cas où le 'form' n'a pas été renseigné et/ou n'ets pas valide
        context = {'bool':bool, 'form':form}
        
    return render(request, 'configSalle/index.html', context)

# def loadjson(request):
    # json_file = open("configSalle/json/confs.json", 'r')
    # json_content = json_file.read()
    # json_file.close()
    # return HttpResponse(
        # json_content,
        # content_type='application/json',
        # status=200   # status_code = OK
    # )