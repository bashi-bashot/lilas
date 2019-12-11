#Algorithme qui sert à trier les tickets de COMMUNICATION
#Extraire les champs importants
#Utiliser les fonctionnalités Django pour créer la base de données

from configSalle.models import Uce, ConfigurationSalle
from django.conf import settings
from datetime import datetime
import os

def main():
    #On ouvre le fichier contenant les tickets
    fic = open(settings.MEDIA_ROOT+"/act_oper.csv", 'r')
    t = fic.readlines() #on stock dans t toutes les lignes du fichier de tickets
    fic.close() #On ferme le flux

# /!\ Reconstruction des tickets pour que chaque u[i] = 1 ticket
    
    u = [''] #u est une liste de tickets
    j=0
    for i in range(len(t)-1): # On parcourt tous les tickets ----- len(t)
        if 'Compte' not in t[i+1]:      #D'où le len(t)-1
            u[j]+=t[i]
        else:
            u[j]+=t[i]
            u.append('') #incrémente la pile pour laisser la place à un nouveau ticket 
            j+=1
    u[j]+=t[len(t)-1]
            
    tic = [] #tic est comme u, à la différence que chaque colonne est un champ du ticket
    
    for i in range(len(u)): #On parcourt tous les tickets ----- len(u)
        tic.append(u[i].replace('\n\n','\n').split('","')) #On sépare les champs de chaque ticket
        
    #print(tic[0][24])
    return tic

    
    
def createConfiguration(t):
    # Fonction qui crée un tableau à 3 cases 
    # t=[ date, "Validation de configuration", configSalle]
    # t=[ id_17, id_18, id_24]
    
    # On enlève les guillemets dans les chaines de caractères des tickets avec le [1:-1]
    for k in range(len(t)):
            
        # On crée une configuration à partir de t
        # On récupère la date au champ 17
        texteDate = t[k][17]
        
        # On récupère l'attribut "Validation de configuration" au champ 18
        validation = t[k][18]

        # On filtre dans les actions l'apparition d'une possible ' ---> ' au vu de notre tic
        actions = t[k][24].replace(' ---> ','')
        
        # On extrait ensuite les secteurs appliqués aux différents UCE
        # pour cela on filtre seulement les actions portant sur les UCEs 
        # dans une liste 'actOper' que l'on va préalablement créer. Chq indice correspond à une actOper
        actOper = []
        if 'Validation de configuration' in validation :
            # print(validation)
            actOper=actions.split('\n')
            if actOper[0][0:4]!='UCE:' and actOper[0][0:5]!=' UCE:' :  #Pour éviter le cas particulier de l'initialisation ie. dans le cas où il n'y a pas de conf UCE.
                pass  #le 'break' nous fait quitter la boucle for
                
            else :
                # On convertit texteDate en datetime
                d = datetime(int(texteDate[6:10]),int(texteDate[3:5]),int(texteDate[0:2]),int(texteDate[12:14]),int(texteDate[15:17]),int(texteDate[18:20]))
                # print(d.strftime("%Y-%m-%d %H:%I:%S"))
                # print(ConfigurationSalle.objects.filter(date=d))
                if ConfigurationSalle.objects.filter(date__contains=d).count()==1:
                    pass                
                else :
                    conf = ConfigurationSalle(date=d)
                    conf.save()
                    # print(actOper[0])
                    i=0
                    for j in range(len(actOper)):
                        if actOper[j][0:4]!='UCE:' and actOper[j][0:5]!=' UCE:' :  #notre filtre est basé sur 'UCE:'
                            i=j                                                    #on détermine l'indice des actions qui nous ne concernent plus
                            # print(i)
                            break
                            
                    for l in range(i):
                        buf = actOper[l].split(':')
                        nom = buf[1][2:-1]
                        sect = buf[3][1:].replace(' contient','')  #on remarque que certains tickets d'UCE n'ont pas la même structure que les autres d'où la suppression du ' contient'
                        # uce=actOper[0].split(':')
                        # print(uce[1][2:-1])
                        # print(uce[3][1:])
                        act = Uce(configurationSalle=conf, nomUce=nom, secteurs=sect)
                        act.save()


    # print(t[0][24])
    return 0
    
    # CODE QUE REALISE LE SCRIPT
tickets = main()
createConfiguration(tickets)


# Commande shell manage.py : exec(open('configSalle/chrgt_conf_salle.py').read())