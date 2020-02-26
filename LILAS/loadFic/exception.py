from django.core.exceptions import *

class FormatError (Exception):
    def __init__(self, format):
        self.format = format
    def __str__(self):
        return repr(self.format)

def test_format(file):
    if '.csv' in file.name:
        # Lorsque le fichier csv est exporté depuis excel ou cree sur un systeme Windows le MIME sera 'application/vnd.ms-excel'
        if file.content_type=='application/vnd.ms-excel' or file.content_type=='text/csv':
            return True
    else:
        raise FormatError("Le format attendu est un fichier CSV")
        return False


class FileError (Exception):
    def __init__(self, error, typeFic):
        self.error = error + typeFic
    def __str__(self):
        return repr(error)

def test_type(file, typeFic):

    # from tempfile import TemporaryFile
    # with TemporaryFile('w+t', encoding='latin-1') as f:
    #     # Lecture/écriture dans le fichier
    #     t=file.readline().decode('latin-1', errors='ignore')
    #     f.write(t)
    #     # Chercher au début et lisez les données
    #     f.seek(0)
    #     donnee = f.read()
    # # Le fichier temporaire est détruit

    donnee = file.readline().decode('latin-1')
    #le codec latin-1 permet de gérer les caractères spéciaux type #donnee = '&é(-è_çà)=)ù%ôÏ *************************************'

    if typeFic == 'elements_systeme':
        t = donnee.split(";")
        print(t)
        print(len(t))
        if len(t)==45:
            return True
        else:
            raise FileError("Veuillez sélectionner un fichier ", typeFic)
            return False
    elif typeFic == 'conf_systeme':
        t = donnee.split(";")
        print(t)
        print(len(t))
        if len(t)==3:
            return True
        else:
            raise FileError("Veuillez sélectionner un fichier ", typeFic)
            return False
    elif typeFic == 'actions_operateur':
        str = "Rapport : Consultation détaillée des actions opérateurs"
    elif typeFic == 'tickets_incident':
        str = "Rapport : Consultation détaillée des tickets d'incidents"
    elif typeFic == 'tickets_de_communication':
        str = "Rapport : Consultation détaillée des tickets de communication"
    
    print('\n******************', str)
    print('\n******************', donnee)

    if str in donnee:
        return True
    else:
        raise FileError("Veuillez sélectionner un fichier ", typeFic)
        return False