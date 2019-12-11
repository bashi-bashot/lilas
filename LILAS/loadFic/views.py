from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import *

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


def index(request):
        
    # formConf = UploadFileForm(request.POST, request.FILES)
    # formSyst = UploadFileForm(request.POST, request.FILES)
    # formOpe = UploadFileForm(request.POST, request.FILES)
    # formCom = UploadFileForm(request.POST, request.FILES)
    # formInc = UploadFileForm(request.POST, request.FILES)  
    
    form = UploadFileForm(request.POST, request.FILES)
    
    # context = {'formConf': formConf, 'formSyst': formSyst, 'formOpe' : formOpe, 'formCom' : formCom, 'formInc' : formInc}
    context = {'form':form}
    
    
    
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
                handle_uploaded_file_ope(request.FILES['fileOpe'])
                context['fileOpe'] = request.FILES['fileOpe'].name

            if 'fileCom' in request.FILES:
                handle_uploaded_file_com(request.FILES['fileCom'])
                context['fileCom'] = request.FILES['fileCom'].name
                
            if 'fileInc' in request.FILES:
                handle_uploaded_file_inc(request.FILES['fileInc'])
                context['fileInc'] = request.FILES['fileInc'].name
                
            return render(request, 'loadFic/upload_is_valid.html', context)
        
        else:
            print('no form valid')
        
    else:
        print('no post') 
        # formConf = UploadFileForm()
        # formOpe = UploadFileForm()
        # formCom = UploadFileForm()
        # formInc = UploadFileForm()
        # form = UploadFileForm() 
    
    return render(request, 'loadFic/index.html', context)

def handle_uploaded_file_conf(f):
    destination = open('communication/ELTS.csv', 'wb+')
    t = f.readlines()
    for i in range(len(t)):
        destination.write(t[i])
    destination.close()
    exec(open('communication/import_num_exterieurs.py').read())
    exec(open('communication/import_num_secteurs.py').read())

def handle_uploaded_file_syst(f):
    destination = open('communication/CONF_SYSTEM.csv', 'wb+')
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
    destination = open('communication/tickets_comm.csv', 'wb+')
    t = f.readlines()
    for i in range(len(t)):
        destination.write(t[i])
    destination.close()
    exec(open('communication/fromCSVtoSQL.py').read())
    
def handle_uploaded_file_inc(f):
    destination = open('incident/tickets_incidents.csv', 'wb+')
    t = f.readlines()
    for i in range(len(t)):
        destination.write(t[i])
    destination.close()
    exec(open('incident/chargement_conf_incidents.py').read())
    
    
def uploadValid(request):
    return render(request, 'loadFic/upload_is_valid.html')