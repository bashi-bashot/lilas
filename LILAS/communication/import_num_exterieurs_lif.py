#Algorithme qui charge les numéros des lifs dans NumExterieur
from communication.models import LIF, NumExterieur

def chargeFichier():
    fic = open("communication/ELTS.csv", 'r')
    tab = fic.readlines()
    fic.close()
    return tab
    
def chercheIndice(t, ind):
    indice = -1
    str_id_elts = ind+',00'
    for j in range(len(t)):
        if t[j][0] == str_id_elts :
            indice = j
    
    return indice
            
    
listeLif = LIF.objects.all()
t = chargeFichier()
#On met en forme t
for i in range(len(t)):
    t[i] = t[i].split(';')
    
for lif in listeLif:
    indice = chercheIndice(t, lif.id_elts)
    if indice != -1: #Si on a bien trouvé une correspondance avec une ligne de elts
        #On cherche la LIF associée
        id_ligne_elts = int(lif.id_elts) + 1
        indice_ligne = chercheIndice(t, str(id_ligne_elts))
        if(indice_ligne != -1) :
            #On a trouvé la line correspondante à la lif
            #On regarde s'il y a un numéro associé
            # print(t[indice][16])
            if len(t[indice][16]) > 2 : 
                #Il y a un targetNumber
                target_number = t[indice][16]
                nomCorr = t[indice_ligne][5].replace('"','')+"_target"
                if NumExterieur.objects.filter(nom__contains=nomCorr).filter(numero__contains=target_number).count() == 0 :
                    corr = NumExterieur(id_lilas = "unknown", id_elts = str(id_ligne_elts), nom=nomCorr, numero = target_number)
                    corr.save()
                else :
                    print("NumExterieur TARGET deja existant")
            # else :
                # print("Absence de Numero TARGET")
            
            # print(t[indice][18])
            if len(t[indice][18])>2 :
                origin_number = t[indice][18]
                nomCorr = t[indice_ligne][5].replace('"','')+"_origin"
                if NumExterieur.objects.filter(nom__contains=nomCorr).filter(numero__contains=origin_number).count() == 0 :
                    corr = NumExterieur(id_lilas = "unknown", id_elts = str(id_ligne_elts), nom=nomCorr, numero = origin_number)
                    corr.save()
                else :
                    print("NumExterieur ORIGIN deja existant ")
                    
            # else :
                # print("Absence de Numero ORIGIN")
        else :
            print("Ligne non trouvée dans ELTS")
            
    else :
        print("LIF non trouvée dans ELTS")
    






#   exec(open('communication/import_num_exterieurs_lif.py').read())
