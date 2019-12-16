from django.core.exceptions import *

class FormatError (Exception):
    def __init__(self, format):
        self.format = format
    def __str__(self):
        return repr(self.format)

def test_format(file):
    if '.csv' in file.name:
        # Lorsque le fichier csv est exporté depuis excel ou créé sur un système Windows le MIME sera 'application/vnd.ms-excel'
        if file.content_type=='application/vnd.ms-excel' or file.content_type=='text/csv':
            return True
    else:
        raise FormatError("Le Format attendu est un fichier CSV")
        return False