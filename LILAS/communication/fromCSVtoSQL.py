#Algorithme qui sert à trier les tickets de COMMUNICATION
#Extraire les champs importants
#Utiliser les fonctionnalités Django pour créer la base de données

from communication.models import *

from django.conf import settings
from datetime import datetime





def main():
    #On ouvre le fichier contenant els tickets
    fic = open("communication/tickets_comm.csv", 'r')
    t = fic.readlines() #on stock dans t toutes les lignes du fichier de tickets --> Chaque ligne EST un ticket
    fic.close() #On ferme le flux
    print(t[0])
    u = [] #u est comme t, à la différence que chaque colonne est un champ du ticket
    
    for i in range(len(t)): #On parcourt tous les tickets ----- len(t)
        u.append(t[i].split(",")) #On sépare les champs du ticket
    return u
    
    
def createAppel(t, listeLif):
    #Fonction qui crée un tableau à 8 cases 
    #t=[appelant, appelé, date, type, durée, libération, line_appelante, line_appelee, etat, fsx_entrant, fsx_sortant, Commentaire(Debord Num ou SU+TP]
    #t=[27,       28,     23,   25,   calcul,        30,               ,             ,   29,         xxx,         xxx,                              31]
    
    #On enlève les guillemets dans les chaines de caractères des tickets avec le [1:-1]
    for k in range(len(t)): 
        print(k)
        #On crée un appel
        #On récupère la date au champ 23
        texteDate = t[k][23].replace('"','')
        texteDateFin = t[k][24].replace('"','')

        #On récupère le nom du joncteur et de l'appelant
        # str = t[k][27][1:-1].replace(" ","") # de la forme -->     Appelant : [PTEL] - EPOS_127              337070   Il faut doint enlever les espaces pour faire le traitement
        # applant = str[len(str)-6:len(str)] #ATTENTION Parfois, le numéro appelant est simplement 0. Si on récupère les 6 derniers caractères, on se retrouve avec un bout de joncteur. --> Si on trouve une lettre dans "appelant" alors il n'a a pas 6 numéros
        # fsx_e = str[9:len(str)-6] # Le faisceau est tout le reste

        #Pour éviter ls problèmes dans le cas d'un numéro qui a moins de 6 chiffres, on peut faire le test suivant :
        #Si on rencontre plus de 5 espace à la fois --> Alors le premier caractère qui n'ets pas un espace qui suit est le premier chiffre du numéro de téléphone
        
        str = t[k][27].replace('"','')
        compteur_espace = 0
        indice_separation = 0
        for l in range(len(str)):
            if(str[l] == ' '):
                compteur_espace = compteur_espace + 1
            else:
                compteur_espace = 0
            
            if(compteur_espace >= 4 ):
                #On est dans à l'indice d'un espace entre le joncteur et le numéro
                indice_separation = l
        
        l = indice_separation
        while (str[l] == ' '): 
            l = l+1
            if(str[l] != ' '):
                #On a rencontré le numéro
                applant = str[l:len(str)]
                fsx_e = str[11:indice_separation-4]
        
        
        #On récupère le nom du joncteur et de l'appelé
        # str2 = t[k][28][1:-1].replace(" ","")
        # apple = str2[len(str2)-6:len(str2)]
        # fsx_a = str2[7:len(str2)-6]
        
        str2 = t[k][28].replace('"','')
        
        compteur_espace = 0
        indice_separation = 0
        for l in range(len(str2)):
            if(str2[l] == ' '):
                compteur_espace = compteur_espace + 1
            else:
                compteur_espace = 0
            
            if(compteur_espace >= 4 ):
                #On est dans à l'indice d'un espace entre le joncteur et le numéro
                indice_separation = l
        
        l = indice_separation
        while (str2[l] == ' '): 
            l = l+1
            if(str2[l] != ' '):
                #On a rencontré le numéro
                apple = str2[l:len(str2)]
                fsx_a = str2[9:indice_separation-4]
        
        #On calcule maintenant la durée de l'appel
        
        
        d = datetime(int(texteDate[6:8])+2000,int(texteDate[3:5]),int(texteDate[0:2]),int(texteDate[9:11]),int(texteDate[12:14]),int(texteDate[15:17]))
        dfin = datetime(int(texteDateFin[6:8])+2000,int(texteDateFin[3:5]),int(texteDateFin[0:2]),int(texteDateFin[9:11]),int(texteDateFin[12:14]),int(texteDateFin[15:17]))
      
        if Appel.objects.filter(date__contains=d).filter(appelant__contains=apple).filter(line_appelante__contains=fsx_e).filter(appele__contains=applant).filter(line_appele__contains=fsx_a).count()==1:
            print(d.__str__()+" "+applant+" "+apple)
            pass
        
        else:
            dur = dfin - d #dur n'est pas un objet datetime, mais un objet timedelta
            
            #Traitemeent sur le champ "ETAT" du ticket : On ne regarde pas ce qui suit 'en'
            
            chaineTemoin = 'en'
            
            chaineATraiter = t[k][29][17:-1]
            
            etatAppel = ''
            for i in range(len(chaineATraiter)-1):
                if (chaineATraiter[i:i+2] == chaineTemoin):
                    etatAppel = chaineATraiter[0:i-1]
                    break
                    
            #On cherche maintenant le nom associé aux numéros dans les annuaires
            tabExterieurs = NumExterieur.objects.all() #On récupère tous les numéros extérieurs
            tabSecteurs = NumSecteur.objects.all() #On récupère tous les numéros de secteurs
            
            num_appelant = applant
            num_appele = apple
            
            nomAppelant =""
            nomAppele=""
                    
                    
            #On regarde si ces deux numéros apparaissent dans la liste des numéros extérieurs ou des numéros de secteurs
            for j in range(len(tabExterieurs)):
                if num_appelant == tabExterieurs[j].numero :
                    nomAppelant = tabExterieurs[j].nom
                    
                    
                if num_appele == tabExterieurs[j].numero :
                    nomAppele = tabExterieurs[j].nom
                    
                
            for j in range(len(tabSecteurs)):
                if num_appelant == tabSecteurs[j].numero :
                    nomAppelant = tabSecteurs[j].nom
                    
                    
                if num_appele == tabSecteurs[j].numero :
                    nomAppele = tabSecteurs[j].nom
                    
            #On vérifie la ligne de tabAlias remplie :
            if nomAppelant == "" :
                nomAppelant = applant
                
            if nomAppele == "" :
                nomAppele = apple
                
            #On récupère maintenant les faisceaux à partir des lignes 
            #fsx_e est la ligne appelante de la forme "[VoIP] - 7H_3_VoIP"
            #fsx_a est la ligne appelee de la forme "[VoIP] - 7H_3_VoIP"
            
            
            
            ligne1 = fsx_e
            ligne2 = fsx_a
            faisceauAppelant = 'fx_xxxx_a'
            faisceauAppele = 'fx_xxxx_e'
            indiceTiret = -1
            indiceFin = -1
            
                #LIGNE - 1
            for i in range(len(ligne1)):
                if ligne1[i] == '-' :
                    indiceTiret = i
                    break
            #l'indice i est '-', l'indice i+1 est ' ' et l'indice i+2 est le début de l'intitulé de la ligne
            # print("indiceTiret :"+str(indiceTiret))
            if(indiceTiret != -1):
                ligne1 = ligne1[i+2:len(ligne1)]
                ligne1 = ligne1.replace(" ", "")
                for p in listeLif :
                    if p.nom == ligne1 :
                        faisceauAppelant = p.faisceau.nom
                        # print("FAISCEAU TROUVE")
                        break;
                    # else :
                        # print("p "+p.nom)
                        # print("l "+ligne1+"plop")
            else :
                print("Erreur détermination LIF")
                
                
            indiceTiret = -1 #On réinitialise le marqueur
                #LIGNE - 2
            for i in range(len(ligne2)):
                if ligne2[i] == '-' :
                    indiceTiret = i
                    break
            #l'indice i est '-', l'indice i+1 est ' ' et l'indice i+2 est le début de l'intitulé de la ligne
            
            if(indiceTiret != -1):
                ligne2 = ligne2[i+2:len(ligne2)]
                ligne2 = ligne2.replace(" ", "")
                for p in listeLif :
                    if p.nom == ligne2 :
                        faisceauAppele = p.faisceau.nom
                        # print("FAISCEAU TROUVE")
                        break;
            else :
                print("Erreur détermination LIF")
                  
                  
            #On s'occupe maintenant de déterminer s'il s'agit d'un appel passé en SU+TP ou d'un débordement Numeris
            sutp = False
            numeris = False
            temo = "SecoursUltime"
            temo2="Numeris"
            
            t[k][31] = t[k][31].replace(" ","")
            
            for l in range(len(t[k][31])-len(temo)):
                if t[k][31][l:l+len(temo)] == temo :
                    sutp = True
                    print("SU+TP")
                    break
            for l in range(len(t[k][31])-len(temo2)):        
                if t[k][31][l:l+len(temo2)] == temo2 :
                    numeris = True
                    print("SDA")
                    break
            
            
            a = Appel(appelant=apple, appele= applant, date = d, type = t[k][25].replace('"',''),duree = int(dur.total_seconds()), liberation = t[k][30][14:-1].replace('"',''), line_appelante = fsx_e, line_appele = fsx_a, etat = etatAppel, nom_appele = nomAppelant , nom_appelant = nomAppele, fx_entrant = faisceauAppele, fx_sortant = faisceauAppelant, SUTP = sutp, SDA = numeris)
            a.save()
      
    return 0
    
    
    #CODE QUE REALISE LE SCRIPT
t = main()
listeLif = LIF.objects.all() #Variable utilisée pour déterminer et référencer le faisceau par lequel passe un appel
createAppel(t, listeLif)


# Commande shell manage.py : exec(open('communication/fromCSVtoSQL.py').read())