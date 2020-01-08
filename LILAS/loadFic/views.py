from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import *
import pytz

# DEBUT import
# INDISPENSABLE pour l'execution de chrgt_conf_salle
# on récupère ceux présents dans ce dernier
from configSalle.models import Uce, ConfigurationSalle
from django.conf import settings
from datetime import datetime

# INDISPENSABLE pour l'execution de incident
from incident.models import Incident

# INDISPENSABLE pour l'execution de communication
from communication.models import *

# Exception Erreur du Format pour le fichier Upload
from .exception import *


def index(request):
    
    form = UploadFileForm(request.POST, request.FILES)
    
    context = {'form':form}
    context['fileOpeError'] = False  
    
    if request.method == 'POST':
        print('post ok')
        if form.is_valid():
            print('\n\n\n****************')
            print(request.FILES)
            print('****************\n\n\n')
            
            if 'fileConf' in request.FILES:
                handle_uploaded_file_conf(request.FILES['fileConf'])
                context['fileConf'] = request.FILES['fileConf'].name
                
            if 'fileSyst' in request.FILES:
                handle_uploaded_file_syst(request.FILES['fileSyst'])
                context['fileSyst'] = request.FILES['fileSyst'].name
            
            if 'fileOpe' in request.FILES:

                try:
                    test_format(request.FILES['fileOpe'])
                except FormatError as e:
                    print('Pb Format :', e.format)
                    context['fileOpeError'] = e.format
                    print(context['fileOpeError'])

                else:
                    print('\n\n\n****************')
                    print('test valid')
                    print('****************\n\n\n')
                    handle_uploaded_file_ope(request.FILES['fileOpe'])
                    context['fileOpe'] = request.FILES['fileOpe']


            if 'fileCom' in request.FILES:
                handle_uploaded_file_com(request.FILES['fileCom'])
                context['fileCom'] = request.FILES['fileCom'].name
                
            if 'fileInc' in request.FILES:
                handle_uploaded_file_inc(request.FILES['fileInc'])
                context['fileInc'] = request.FILES['fileInc'].name

            if len(context)>2:
                print('\n\n\n****************')
                print(len(context))
                print('****************\n\n\n')    
                return render(request, 'loadFic/upload_is_valid.html', context)
        
        else:
            print('no form valid')
        
    else:
        print('no post') 

    return render(request, 'loadFic/index.html', context)

def handle_uploaded_file_conf(f):
    with open(settings.MEDIA_ROOT+'/ELTS.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    exec(open('communication/import_num_exterieurs.py').read())
    exec(open('communication/import_num_secteurs.py').read())

def handle_uploaded_file_syst(f):
    destination = open(settings.MEDIA_ROOT+'/CONF_SYSTEM.csv', 'wb+')
    t = f.readlines()
    for i in range(len(t)):
        destination.write(t[i])
    destination.close()
    exec(open('communication/loadFX.py').read())
    exec(open('communication/import_num_exterieurs_lif.py').read())
    
def handle_uploaded_file_ope(f):
    with open(settings.MEDIA_ROOT+'/act_oper.csv', 'wb+') as destination:
        # en appelant la methode Uploadfil.chunks() au lieu de read(), on peut s’assurer que les gros fichiers ne saturent pas la mémoire du système.
        for chunk in f.chunks():
            destination.write(chunk)

    # destination = open('configSalle/act_oper.csv', 'wb+')
    # t = f.readlines()
    # for i in range(len(t)):
    #     destination.write(t[i])
    # destination.close()
    exec(open('configSalle/chrgt_conf_salle.py').read())
    
def handle_uploaded_file_com(f):
    with open(settings.MEDIA_ROOT+'/tickets_comm.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    exec(open('communication/fromCSVtoSQL.py').read())
    
def handle_uploaded_file_inc(f):
    with open(settings.MEDIA_ROOT+'/tickets_incidents.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    exec(open('incident/chargement_conf_incidents.py').read())
    
    
def uploadValid(request):
    return render(request, 'loadFic/upload_is_valid.html')