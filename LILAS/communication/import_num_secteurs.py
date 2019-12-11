#Algorithme qui charge en base de donnée les numéros extérieurs au CRNA.
from communication.models import NumExterieur
from communication.models import NumSecteur
from django.conf import settings

def chargeFichier():
    fic = open(settings.MEDIA_ROOT+"/ELTS.csv", 'r')
    tab = fic.readlines()
    fic.close()
    return tab #Chaque élément de tab est une ligne de ELTS
    
def chercheATC(t):
    temoin="SECT"
    indexOfSECT=[]
    for i in range(len(t)):
        for j in range(len(t[i])-4):
            if(t[i][j:j+4] == temoin):
                indexOfSECT.append(i)
                
    return indexOfSECT
    
t = chargeFichier()
tabIndex = chercheATC(t)

for i in tabIndex :
    t[i] = t[i].split(';')

for i in range(len(tabIndex)):
    id_floating = str(t[tabIndex[i]][0]) #id_elts (string) avec deux 0 après la virgule
    id = id_floating[0:len(id_floating)-3] #virgule et chiffres après la virgule enlevés
    
    if NumSecteur.objects.filter(numero__contains=str(t[tabIndex[i]][32])).filter(nom__contains=t[tabIndex[i]][5][1:-1]).count()==0:
        corr = NumSecteur(id_elts =id , id_lilas = str(i), numero = str(t[tabIndex[i]][32]), nom = t[tabIndex[i]][5][1:-1])
        corr.save()
    else:
        print("Doublons numero secteur")
    

# Commande shell manage.py : exec(open('communication/import_num_secteurs.py').read())