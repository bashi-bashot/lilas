#Algorithme qui sert à trier les tickets de COMMUNICATION
#Extraire les champs importants
#Utiliser les fonctionnalités Django pour créer la base de données

from communication.models import Appel
from django.conf import settings
from datetime import datetime
import os
os.remove("test_u2.txt")

def main():
    #On ouvre le fichier contenant les tickets
    fic = open("configSalle/act_oper.csv", 'r')
    t = fic.readlines() #on stock dans t toutes les lignes du fichier de tickets
    fic.close() #On ferme le flux

    # for i in range(36):   # On visualise t dans un fichier txt pour voir la construction des tickets dans la liste
        # if t[i]!='\n':
            # fichier = open("test.txt", 'a')
            # fichier.write(t[i])
            # fichier.close()
    
# /!\ Reconstruction des tickets pour que chaque u[i] = 1 ticket
    
    u = [''] #u est une liste de tickets
    j=0
    for i in range(len(t)-1): # On parcourt tous les tickets ----- len(t)
        if 'Compte' not in t[i+1]:      #D'où le len(t)-1
            u[j]+=t[i]
        else:
            u[j]+=t[i]
            u.append('')
            j+=1
    u[j]+=t[len(t)-1]
    
    for i in range(len(u)):
            fichier = open("test_u2.txt", 'a')
            fichier.write(u[i].replace('\n\n','\n'))
            fichier.close()
            
    tic = [] #tic est comme u, à la différence que chaque colonne est un champ du ticket
    for i in range(len(u)): #On parcourt tous les tickets ----- len(u)
        tic.append(u[i].replace('\n\n','\n').split(",")) #On sépare les champs de chaque ticket
    print(tic[0])    
    return tic

    
    
# def createAppel(t):
    # # Fonction qui crée un tableau à 3 cases 
    # # t=[ date, "Validation de configuration", configSalle]
    # # t=[ id_17, id_18, id_24]
    
    # # On enlève les guillemets dans les chaines de caractères des tickets avec le [1:-1]
    # for k in range(len(t)): 
            
        # # On crée un appel
        # # On récupère la date au champ 23
        # texteDate = t[k][23][1:-1]
        # texteDateFin = t[k][24][1:-1]

        # # On récupère le nom du joncteur et de l'appelant
        # # str = t[k][27][1:-1].replace(" ","") # de la forme -->     Appelant : [PTEL] - EPOS_127              337070   Il faut doint enlever les espaces pour faire le traitement
        # # applant = str[len(str)-6:len(str)] #ATTENTION Parfois, le numéro appelant est simplement 0. Si on récupère les 6 derniers caractères, on se retrouve avec un bout de joncteur. --> Si on trouve une lettre dans "appelant" alors il n'a a pas 6 numéros
        # # fsx_e = str[9:len(str)-6] # Le faisceau est tout le reste

        # # Pour éviter ls problèmes dans le cas d'un numéro qui a moins de 6 chiffres, on peut faire le test suivant :
        # # Si on rencontre plus de 5 espace à la fois --> Alors le premier caractère qui n'ets pas un espace qui suit est le premier chiffre du numéro de téléphone
        
        # str = t[k][27][1:-1]
        # compteur_espace = 0
        # indice_separation = 0
        # for l in range(len(str)):
            # if(str[l] == ' '):
                # compteur_espace = compteur_espace + 1
            # else:
                # compteur_espace = 0
            
            # if(compteur_espace >= 4 ):
                # # On est dans à l'indice d'un espace entre le joncteur et le numéro
                # indice_separation = l
        
        # l = indice_separation
        # while (str[l] == ' '): 
            # l = l+1
            # if(str[l] != ' '):
                # # On a rencontré le numéro
                # applant = str[l:len(str)]
                # fsx_e = str[11:indice_separation-4]
        
        
        # # On récupère le nom du joncteur et de l'appelé
        # # str2 = t[k][28][1:-1].replace(" ","")
        # # apple = str2[len(str2)-6:len(str2)]
        # # fsx_a = str2[7:len(str2)-6]
        
        # str2 = t[k][28][1:-1]
        
        # compteur_espace = 0
        # indice_separation = 0
        # for l in range(len(str2)):
            # if(str2[l] == ' '):
                # compteur_espace = compteur_espace + 1
            # else:
                # compteur_espace = 0
            
            # if(compteur_espace >= 4 ):
                # # On est dans à l'indice d'un espace entre le joncteur et le numéro
                # indice_separation = l
        
        # l = indice_separation
        # while (str2[l] == ' '): 
            # l = l+1
            # if(str2[l] != ' '):
                # # On a rencontré le numéro
                # apple = str2[l:len(str2)]
                # fsx_a = str2[11:indice_separation-4]
        
        # # On calcule maintenant la durée de l'appel
        # d = datetime(int(texteDate[6:8])+2000,int(texteDate[3:5]),int(texteDate[0:2]),int(texteDate[9:11]),int(texteDate[12:14]),int(texteDate[15:17]))   
        # dfin = datetime(int(texteDateFin[6:8])+2000,int(texteDateFin[3:5]),int(texteDateFin[0:2]),int(texteDateFin[9:11]),int(texteDateFin[12:14]),int(texteDateFin[15:17]))
      
        # dur = dfin - d #dur n'est pas un objet datetime, mais un objet timedelta
        
        # a = Appel(appelant=applant, appele= apple, date = d, type = t[k][25][1:-1],duree = int(dur.total_seconds()), liberation = t[k][30][14:-1], fsx_appelant= fsx_e,  fsx_appele = fsx_a)
       
        # a.save()
      
    # return 0
    
    
    #CODE QUE REALISE LE SCRIPT
tic = main()
# createAppel(tic)


# Commande shell manage.py : exec(open('configSalle/chrgt_conf_salle_2.py').read())