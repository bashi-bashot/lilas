#Script qui charge les faisceaux et les lignes
#Charge aussi certaines LIF qui interviennent dans les appels
from communication.models import Faisceau, LIF
from django.conf import settings



def chargeFichier():
    fic = open(settings.MEDIA_ROOT+"/ELTS.csv", 'r')
    tab = fic.readlines()
    fic.close()
    return tab #Chaque élément de tab est une ligne de ELTS
    
def chercheFX(t):
    temoin="FX"
    indexOfFX=[]
    for i in range(len(t)):
        u = t[i].split(';')
        for j in range(len(u[1])-2):
            if(u[1][j:j+2] == temoin):
                indexOfFX.append(i)
    return indexOfFX
    
def chercheLif(t):
    temoin=';"LIF '
    indexOfLif=[]
    for i in range(len(t)):
        
        # print(u)
        for j in range(len(t[i])-10):
            if(t[i][j:j+len(temoin)] == temoin):
                indexOfLif.append(i)
    return indexOfLif
    
    
t = chargeFichier()
tabIndex = chercheFX(t)
tabIndexLif=chercheLif(t)

for i in tabIndex :
    t[i] = t[i].split(';')
    
# print(t[0])

for i in range(len(tabIndex)):
    id_floating = str(t[tabIndex[i]][0]) #id_elts (string) avec deux 0 après la virgule
    id = id_floating[0:len(id_floating)-3] #virgule et chiffres après la virgule enlevés
    
    if Faisceau.objects.filter(nom__contains=t[tabIndex[i]][5][1:-1]).count()==0:
        fx = Faisceau(id_elts =id , id_lilas = str(i), nom = t[tabIndex[i]][5][1:-1])
        fx.save()
    else :
        print('fx deja present')
    

#On s'occupe maintenant des LIFs

print("indices des LIFS recuperes : "+str(len(tabIndexLif)))

f = open(settings.MEDIA_ROOT+"/CONF_SYSTEM.csv", 'r')
tabLien = f.readlines()
f.close()

tabFaisceaux = Faisceau.objects.all()
print("Chargement des faisceaux")

#On commence par mettre en forme le tableau de lien
for i in tabLien :
    i=i.split(';')
    i[1] = i[1][0:len(i[1])-3] #On enlève les la virgule et les chiffres après la virgule
    i[2] = i[2][0:len(i[2])-4] #On enlève les la virgule et les chiffres après la virgule et le \n

    #On cherche dans te tableau CONF_SYSTEM si on trouve une correspondance

for i in tabIndexLif :
    t[i] = t[i].split(';')

for i in range(len(tabIndexLif)):
    id_floating = str(t[tabIndexLif[i]][0]) #id_elts (string) avec deux 0 après la virgule
    id = id_floating[0:len(id_floating)-3] #virgule et chiffres après la virgule enlevés
    # print(id)
    id_fx = '-1'
    #On regarde s'il existe un élément de type_association : 24 qui lie le numéro de LIF avec un numéro de faisceau
    for k in tabLien :
        k = k.split(";")
        # print(k[0])
        if k[0] == '24' :
            if k[2][0:len(k[2])-4] == str(id) : #Si on trouve l'id_elts d'une LIF dans le tableau d'association, alors il faut regarder l'id_elts du faisceau
                id_fx = k[1][0:len(k[1])-3]
                # print("Faisceau trouvé avec l'id : "+id_fx)
    
    fxLifCourrant = ""
    if id_fx == '-1' :
        # print("Faisceau non trouve")
        pass
    else :
        # print("LIF : Faisceau trouvé")
        #On récupère le faisceau correspondant dans la table Faisceau
        for faisceau in tabFaisceaux :
            if faisceau.id_elts == id_fx :
                fxLifCourrant = faisceau
                break;
        if fxLifCourrant != "" :        
            if LIF.objects.filter(nom__contains=t[tabIndexLif[i]][5][1:-1]).count()==0:
                lif = LIF(id_elts =id , id_lilas = str(i), nom = t[tabIndexLif[i]][5][1:-1], faisceau = fxLifCourrant)
                lif.save()
            else:
                print('lif deja présente')
    
#On s'occupe maintenant des LIFs orphelines 
#On crée un faisceau fictif
nomFx = "Fx FICTIF"
faisc = Faisceau(nom = nomFx, id_elts="abcd", id_lilas='abcd')
if Faisceau.objects.filter(nom__contains=nomFx).count()==0:
    faisc.save()
else :
    print("Faisceau fictif deja existant")
#Pour chaque élément de TabIndexLIF on crée une LIF. Au pire, elle existe déjà

#On doit déterminer le dernier id id_lilas attribué
listeLifExistantes = LIF.objects.all()
maxID = -1
for i in range(len(listeLifExistantes)):
    if int(listeLifExistantes[i].id_lilas) > maxID :
        maxID = int(listeLifExistantes[i].id_lilas)
    
    
for p in tabIndexLif :
    # print(t[p][1].replace('"','').replace(' ',''))
    # print(t[p][5].replace('"',''))
    maxID = maxID + 1
    l = LIF(nom = t[p][5].replace('"',''), faisceau = faisc, id_elts = t[p][0][0:len(t[p][0])-3], id_lilas = maxID)
    if LIF.objects.filter(id_elts__contains=t[p][0][0:len(t[p][0])-3]).count() == 0 :
        l.save()
    else :
        print("LIF déjà existante")
    
    
    
    
    

# Commande shell manage.py : exec(open('communication/loadFX.py').read())