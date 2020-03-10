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

# Exception Erreur du Format/Type pour le fichier Upload
from .exception import *

#Variable globale
global context
context = {}

def index(request):
    
    form = UploadFileForm(request.POST, request.FILES)
    print('++++++++++++++++++++++form+++++++++++++++++++++')
    
    global context
    context = {'form':form}
    context['fileEltsError'] = False
    context['fileSystError'] = False
    context['fileOpeError'] = False
    context['fileComError'] = False
    context['fileIncError'] = False

    if request.method == 'POST':
        print('post ok')
        if form.is_valid():
            print('\n\n\n****************')
            print(request.FILES)
            print('****************\n\n\n')
            
            if 'fileConf' in request.FILES:
        
                try:
                    test_format(request.FILES['fileConf'])
                except FormatError as e:
                    print('Pb Format :', e.format)
                    context['fileEltsError'] = e.format
                    print(context['fileEltsError'])

                else:
                    print('\n\n\n****************')
                    print('test format valid')
                    print('****************\n\n\n')
                    handle_uploaded_file_conf(request.FILES['fileConf'])
                    context['fileConf'] = request.FILES['fileConf'].name
                
            if 'fileSyst' in request.FILES:

                try:
                    test_format(request.FILES['fileSyst'])
                except FormatError as e:
                    print('Pb Format :', e.format)
                    context['fileSystError'] = e.format
                    print(context['fileSystError'])

                else:
                    print('\n\n\n****************')
                    print('test format valid')
                    print('****************\n\n\n')
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
                    print('test format valid')
                    print('****************\n\n\n')
                    handle_uploaded_file_ope(request.FILES['fileOpe'])
                    context['fileOpe'] = request.FILES['fileOpe']


            if 'fileCom' in request.FILES:
                try:
                    test_format(request.FILES['fileCom'])
                except FormatError as e:
                    print('Pb Format :', e.format)
                    context['fileComError'] = e.format
                    print(context['fileComError'])

                else:
                    print('\n\n\n****************')
                    print('test format valid')
                    print('****************\n\n\n')
                    handle_uploaded_file_com(request.FILES['fileCom'])
                    context['fileCom'] = request.FILES['fileCom'].name
                
            if 'fileInc' in request.FILES:
                try:
                    test_format(request.FILES['fileInc'])
                except FormatError as e:
                    print('Pb Format :', e.format)
                    context['fileIncError'] = e.format
                    print(context['fileIncError'])

                else:
                    print('\n\n\n****************')
                    print('test format valid')
                    print('****************\n\n\n')
                    handle_uploaded_file_inc(request.FILES['fileInc'])
                    context['fileInc'] = request.FILES['fileInc'].name

            # if len(context)>6:
            #     print('\n\n\n****************')
            #     print(len(context))
            #     print('****************\n\n\n')
            #     print(context)
            if context['fileOpeError'] or context['fileComError'] or context['fileIncError'] or context['fileEltsError'] or context['fileSystError'] != False:
                # HttpResponseRedirect('/loadFic/')
                return render(request, 'loadFic/index.html', context)
            else:
                return render(request, 'loadFic/upload_is_valid.html', context)
        
        else:
            print('no form valid')
        
    else:
        print('no post') 

    return render(request, 'loadFic/index.html', {'form':form})



def handle_uploaded_file_conf(f):
    global context

    try:
        test_type(f, 'elements_systeme')
    except FileError as e:
        print('Pb Type :', e.error)
        context['fileEltsError'] = e.error
        print(context['fileEltsError'])

    else:
        print('\n\n\n****************')
        print('test type valid')
        print('****************\n\n\n') 
        with open(settings.MEDIA_ROOT+'/ELTS.csv', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        exec(open('communication/import_num_exterieurs.py').read())
        exec(open('communication/import_num_secteurs.py').read())

def handle_uploaded_file_syst(f):
    global context

    try:
        test_type(f, 'conf_systeme')
    except FileError as e:
        print('Pb Type :', e.error)
        context['fileSystError'] = e.error
        print(context['fileSystError'])

    else:
        print('\n\n\n****************')
        print('test type valid')
        print('****************\n\n\n')
        with open(settings.MEDIA_ROOT+'/CONF_SYSTEM.csv', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        exec(open('communication/loadFX.py').read())
        exec(open('communication/import_num_exterieurs_lif.py').read())
    

def handle_uploaded_file_ope(f):
    global context

    # destination = open('configSalle/act_oper.csv', 'wb+')
    # t = f.readlines()
    # for i in range(len(t)):
    #     destination.write(t[i])
    # destination.close()

    # file=f.readlines()
    # print(file)

    try:
        test_type(f, 'actions_operateur')
    except FileError as e:
        print('Pb Type :', e.error)
        context['fileOpeError'] = e.error
        print(context['fileOpeError'])

    else:
        print('\n\n\n****************')
        print('test type valid')
        print('****************\n\n\n')
        with open(settings.MEDIA_ROOT+'/act_oper.csv', 'wb+') as destination:
        # en appelant la methode Uploadfil.chunks() au lieu de read(), on peut s’assurer que les gros fichiers ne saturent pas la mémoire du systeme.
            for chunk in f.chunks():
                destination.write(chunk)
        exec(open('configSalle/chrgt_conf_salle.py').read())
    
    
def handle_uploaded_file_com(f):
    global context

    try:
        test_type(f, 'tickets_de_communication')
    except FileError as e:
        print('Pb Type :', e.error)
        context['fileComError'] = e.error
        print(context['fileComError'])

    else:
        print('\n\n\n****************')
        print('test type valid')
        print('****************\n\n\n') 
        with open(settings.MEDIA_ROOT+'/tickets_comm.csv', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        exec(open('communication/fromCSVtoSQL.py').read())
    
def handle_uploaded_file_inc(f):
    global context

    try:
        test_type(f, 'tickets_incident')
    except FileError as e:
        print('Pb Type :', e.error)
        context['fileIncError'] = e.error
        print(context['fileIncError'])

    else:
        print('\n\n\n****************')
        print('test type valid')
        print('****************\n\n\n')
        with open(settings.MEDIA_ROOT+'/tickets_incidents.csv', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        exec(open('incident/chargement_conf_incidents.py').read())
    
    
def uploadValid(request):
    return render(request, 'loadFic/upload_is_valid.html')