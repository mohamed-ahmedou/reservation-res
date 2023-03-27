from ast import Or
from genericpath import exists
from multiprocessing import context
from django.forms import inlineformset_factory
from webbrowser import Opera
from xmlrpc.client import boolean
from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate ,login  , logout 
from datetime import *
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import * 
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

import requests
from django.conf import settings
from django.contrib import messages
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------Debut Fonction Partie Admin ou Agent-------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
##-------------------------------------------------------------Fonction admin ou agent-----------------------------------------------------------------


def choix_table(request):
    return render(request , 'Reservation/ChoissizeTableType.html')

def choix_salle(request):
    return render(request , 'Reservation/Choisissez_type_salle.html')
# admin
def choix_salle_admin(request):
    return render(request , 'Reservation/Choisissez_type_salle_admin.html')
def choix_table_admin(request):
    return render(request , 'Reservation/Choisissez_type_table_admin.html')

    

#------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------- Fonction Navbar---------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
# def login(request):
#     if request.method == "POST":
#         user = request.POST['username']
#         passs = request.POST['password']
#         user = authenticate(username=user, password=passs)
#         if user is not None:
#             if user.is_superuser:
                
#                 return redirect("/home")
#         else:   
#             msg = "Les données sont  erronés,ressayer"
#             return render(request, "Reservation/Login.html", {"msg":msg})
    
#     return render (request, 'Reservation/Login.html')

def register(request):   
            form = CreateNewUser()
            if request.method == 'POST': 
                   form = CreateNewUser(request.POST)
                   if form.is_valid():

                       recaptcha_response = request.POST.get('g-recaptcha-response')
                       data = {
                           'secret' : settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                           'response' : recaptcha_response
                       }
                       r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
                       result = r.json()
                       if result['success']:
                           user = form.save()
                           username = form.cleaned_data.get('username')
                           messages.success(request , username + ' creer avec  Successe !')
                           return redirect('login')
                       else:
                          messages.error(request ,  ' invalid Recaptcha please try again!')  
 
        
            context = {'form':form}

            return render(request , 'Reservation/Registre.html', context )



def userLogin(request):  

        if request.method == 'POST': 
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request , username=username, password=password)
            if user is not None:
             login(request, user)
             return redirect('home')
            else:
                messages.info(request, "Erreur d'information")
    
        context = {}

        return render(request , 'Reservation/login.html', context )

#----------------------regitre


#--------------------------------------------------------------------Home---------------------------------------------------------------------------

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        client = Client.objects.all()
        table = Table.objects.all()
        salle = Salle.objects.all()
        resrevation_table = Reservation_table.objects.all()
        resrevation_salle = Reservation_salle.objects.all()
        nb_client = Client.objects.all().count()
        nb_table = Table.objects.all().count()
        nb_salle = Salle.objects.all().count()
        nb_reservation_table = Reservation_table.objects.all().count()
        nb_reservation_salle = Reservation_salle.objects.all().count()
        nb_table_non_reserver = nb_table - nb_reservation_table
        nb_salle_non_reserver = nb_salle - nb_reservation_salle
        totale_reservations = nb_reservation_table + nb_reservation_salle
        context = {'client' : client,
                'table': table,
                'salle': salle,
                'resrevation_table' : resrevation_table,
                'resrevation_salle' : resrevation_salle,
                'nb_client' : nb_client,
                'nb_table' : nb_table,
                'nb_salle' : nb_salle,
                'nb_reservation_table' : nb_reservation_table,
                'nb_reservation_salle' : nb_reservation_salle,
                'totale_reservations':totale_reservations,
                'nb_table_non_reserver':nb_table_non_reserver,
                'nb_salle_non_reserver' : nb_salle_non_reserver}
        return render (request,'Reservation/Tabledebord.html ',context)


#----------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------fonction Reservations--------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------Reservation--------------------------------------------------


def reservation(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        salle = Reservation_salle.objects.all()
        table = Reservation_table.objects.all()
        context = {'salle' : salle,
                'table' : table}
        return render( request, 'Reservation/Reservation.html',context)

      
#--------------------------------------------------------------Reservation-salle--------------------------------------------------

def reservation_salle(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        reserv_salle = Reservation_salle.objects.all()
        return render (request, 'Reservation/Reservation_salle.html',{'reserv_salle' : reserv_salle})


#--------------------------------------------------------------Reservation-table--------------------------------------------------

def reservation_table(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        reserv_table = Reservation_table.objects.all()
        return render(request, 'Reservation/Reservation_Table.html',{'reserv_table' : reserv_table})
        
      
#--------------------------------------------------------------Reservation-salle-table--------------------------------------------------


# def reservation_salle_table(request):       
#     salle = Reservation_salle.objects.all()
#     table = Reservation_table.objects.all()
#     context = {'salle' : salle,
#                'table' : table}
#     return render( request, 'Reservation/Reservation_salle_table.html',context)




#---------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------salle----------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------

def salle(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else: 
        salle = Salle.objects.all()
        res_salle = Reservation_salle.objects.all()
        for s in res_salle:
            n = s.salle.id
            print(n)
        reservation = {'salle':salle,
                    'res_salle' : res_salle,
                    
                    'Reserver' : "Reserver",
                    'Non_Reserver' : "Non Reserver"}
        return render(request, 'Reservation/Salle.html',reservation) 
 
     
#------------------------------------------------------------------table----------------------------------------------------------------

def table(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        table = Table.objects.all()
        res_table = Reservation_table.objects.all()
        for k in  res_table:
            l = k.table.id
            print(l)
        context = {'table':table,
                
               
                }
        return render(request, 'Reservation/Table.html',context) 




#--------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------client----------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------

def client(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        client = Client.objects.all()
        return render(request, 'Reservation/Client.html',{'client':client})






#----------------------------------------------------------------------------------------------------------------------------------------------------
#-----°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°---------------------------- FONCTION DE L'AJOUT--------°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------
def ajout_client(request):
    if request.method=="POST":   
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        email = request.POST['email']
        tel = request.POST['tel']
        c = Client.objects.create(nom=nom, prenom = prenom, email=email, tel=tel )
        c.save()
        return redirect("/client")
    
    return render(request, 'Reservation/Ajout_client.html')

#----------------------------------------------------------------ajout une salle--------------------------------------

def ajout_salle(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method=="POST":   
            numero = request.POST['numero']
            type = request.POST['type']
            c = Salle.objects.create(numero=numero, type = type )
            c.save()
            return redirect("/salle")
        
        return render(request, 'Reservation/ajout_salle.html')


#-----------------------------------------------------------------ajout une table -------------------------------------------


def ajout_table(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method=="POST":   
            numero = request.POST['numero']
            type = request.POST['type']
            iddd = request.POST['idd']
            salle = Salle.objects.get(id=iddd)
            numero_exist = Table.objects.filter(numero=numero).exists()
            print('type de tables est: ',type)
            print('type de salle est: ',salle.type)
            print("le numero est : ", numero)
            print("le numero exist est : ", numero_exist)
            if type != salle.type:
            #    return render (request, )
               msg = "Erreur , Table Vip doit etre ajouter dans Salle Vip!"
               salles = Salle.objects.all()
               return render(request, "Reservation/ajout_table.html", {"msg":msg,'salles' : salles})
            elif numero_exist:
               msg = "Erreur , Table Exist deja"
               salles = Salle.objects.all()
               return render(request, "Reservation/ajout_table.html", {"msg":msg,'salles' : salles})
                
            c = Table.objects.create(numero=numero, type=type, salle=salle )
            c.save()
            return redirect("/table")
        salles = Salle.objects.all()
        return render(request, 'Reservation/ajout_table.html',{'salles' : salles})


#-------------------------------------------------ajout reservation salle---------------------------------------------------------


def ajout_reservation_salle(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        if request.method=="POST":   
            nom = request.POST['nom']
            prenom = request.POST['prenom']
            tel = request.POST['tel']
            email = request.POST['email']
            iddd = request.POST['idd']
            date_reservation = request.POST['date_reservation']
            salle = Salle.objects.get(id=iddd)
            client = Client.objects.create(nom=nom, prenom=prenom, tel=tel, email=email)
            r = Reservation_salle.objects.create(client = client, salle=salle, date_reservation = date_reservation)
            client.save()
            r.save()
            idd = r.id 
            nom = Reservation_salle.objects.all()
            return render (request, 'Reservation/impression_salle_admin.html', {'idd': idd}) 
        salles = Salle.objects.all()
        return render(request, 'Reservation/Ajout_reservation_salle.html',{'salles':salles})


#--------------------------------------------------ajout reservation table------------------------------------


def ajout_reservation_table(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method=="POST":   
            nom = request.POST['nom']
            prenom = request.POST['prenom']
            tel = request.POST['tel']
            email = request.POST['email']
            iddd = request.POST['idd']
            date_reservation = request.POST['date_reservation']
                
            table = Table.objects.get(id=iddd)
            
            client = Client.objects.create(nom=nom, prenom=prenom, tel=tel, email=email)
            r = Reservation_table.objects.create(client = client, table=table, date_reservation = date_reservation )
            client.save()
            r.save() 
            idd = r.id
            return render(request, 'Reservation/impression_table_admin.html',{'idd': idd}) 
            
        tables = Table.objects.all()
        return render(request,'Reservation/Ajout_reservation_table.html',{'tables' : tables} )


#---------------------------------------------------------------------------------------------------------------
#-----°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°--------- FONCTION DE MODIFICATION--------°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°-----------------
#------------------------------------------------------------------------------------------------------------------

#----------------------------------------------Modifier Client ---------------------------------------------

def modifier_client(request, myid):
    if not request.user.is_authenticated:
        return redirect('login')
    else:

        cl = Client.objects.get(id=myid)
        if request.method=="POST":   
            cl.nom = request.POST['nom']
            cl.prenom = request.POST['prenom']
            cl.email = request.POST['email']
            cl.tel = request.POST['tel']
            cl.save()
            return redirect("/client")  
        return render(request, 'Reservation/Modifier_client.html', {'cl': cl}) 

#---------------------------------------------Modifier salle-------------------------------------------------------

def modifier_salle(request, myid):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        v = Salle.objects.get(id=myid)
        if request.method=="POST":   
            v.numero = request.POST['numero']
            v.type = request.POST['type']
            v.save()
            return redirect("/salle")  
        return render(request, 'Reservation/Modifier_salle.html', {'v': v})


#-----------------------------------------------modifier table------------------------------------------------------------------

def modifier_table(request, myid):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        t = Table.objects.get(id=myid)
        if request.method=="POST":   
            t.numero = request.POST['numero']
            t.type = request.POST['type']
            idddd = request.POST['idd']
            salle = Salle.objects.get(id=idddd)
            print(t.numero)
            t.salle = salle
            t.save()
            print(t.numero)
            return redirect("/table")
    s = Salle.objects.all() 
    return render(request, 'Reservation/Modifier_table.html',{'s' : s, 't' : t})


#-----------------------------------------------modifier reservation-salle-----------------------------#--


def modifier_reservation_salle(request, myid):
    if not request.user.is_authenticated:
        return redirect('login')
    else:

        S = Reservation_salle.objects.get(id=myid) 
    
        if request.method == "POST":
            S.client.nom = request.POST['nom']
            S.client.prenom = request.POST['prenom']
            S.client.tel = request.POST['tel']
            S.client.email = request.POST['email']
            S.date_reservation = request.POST['date_reservation']
            idddd = request.POST['idd']
            S.sal = Salle.objects.get(id=idddd)
            print(S.salle.numero)
            S.salle = S.sal
            S.save()
            
            return redirect("/reservation_salle")
            salle = Salle.objects.all() 
            return render(request, 'Reservation/Modifier_reservation_salle.html',{'salle' : salle,'S': S})




#---------------------------------------------------------------------------------------------------------------
#-----------------------------------------------FONCTION SUPPRESSION-------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------



#-----------------------------------------------supprimer un client ---------------------------------------


def supprimer_client(request, myid):
    if not request.user.is_authenticated:
        return redirect('login')
    else:

        client = Client.objects.filter(id=myid)
        client.delete()
        return redirect("/client") 



#-----------------------------------------------supprimer une salle ---------------------------------------

def supprimer_salle(request, myid):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        salle = Salle.objects.filter(id=myid)
        salle.delete()
        return redirect("/salle")  


#-----------------------------------------------supprimer une table ---------------------------------------


def supprimer_table(request, myid):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        table = Table.objects.filter(id=myid)
        table.delete()
        return redirect("/table")  
    
    

def supprimer_reservation_salle(request, myid):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        res = Reservation_salle.objects.filter(id=myid)
        res.delete()
        return redirect("/reservation_salle")
    
 
 
#-----------------------------------------------supprimer reservation table ---------------------------------------
 

def supprimer_reservation_table(request, myid):
    if not request.user.is_authenticated:
        return redirect('login')
    else:

        res = Reservation_table.objects.filter(id=myid)
        res.delete()
        return redirect("/reservation_table")  

#-----------------------------------------------supprimer reservation salle table---------------------------------------


def supprimer_reservation_salle_table(request, myid,mid):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        res_s = Reservation_salle.objects.filter(id=myid)
        res_t = Reservation_table.objects.filter(id=mid)
        res_s.delete()
        res_t.delete()
        return redirect("/reservation_salle_table")  



#------------------------------------------------------------------------------------------------------
#------------------------------------------------FONCTION RECHCERCHE-----------------------------------------
#------------------------------------------------------------------------------------------------------


#------------------------------------------------recherche client-----------------------------------------

def rechercher_client(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method=="POST":
            tel = request.POST['tel']  
            try:
                re = Client.objects.get(tel = tel)
                print(re.nom)
                context ={'tel' : tel,
                        're' : re}
                return render(request, 'Reservation/Rechercher_client.html',context)
            except:
                return render(request, 'Reservation/Rechercher_client.html',{})
        else: 
            return render(request, 'Reservation/Rechercher_client.html',{})
        

#-------------------------------------------------recherche salle-----------------------------------------

def rechercher_salle(request):
    if request.method=="POST":
        numero = request.POST['numero']  
        try:
            re = Salle.objects.get(numero = numero)
            print(re.numero)
            salle = Salle.objects.all()
            res_salle = Reservation_salle.objects.all()
            context = {'numero' : numero,
                     're' : re,
                     'salle':salle,
                    'res_salle' : res_salle,
                    'Reserver' : "Reserver",
                    'Non_Reserver' : "Non Reserver"}
            
            return render(request, 'Reservation/Rechercher_salle.html',context)
        except:
           return render(request, 'Reservation/Rechercher_salle.html',{})
    else: 
        return render(request, 'Reservation/Rechercher_salle.html',{})
    
    
#------------------------------------------------recherche table-----------------------------------------

def rechercher_table(request):
    if request.method=="POST":
        numero = request.POST['numero']  
        try:
            re = Table.objects.get(numero = numero)
            print(re.numero)
            context ={'numero' : numero,
                     're' : re}
            return render(request, 'Reservation/Rechercher_table.html',context)
        except:
           return render(request, 'Reservation/Rechercher_table.html',{})
    else: 
        return render(request, 'Reservation/Rechercher_table.html',{})


#------------------------------------------------recherche reservation salle-----------------------------------------

def rechercher_reservation_salle(request):
    if request.method=="POST":
        tel = request.POST['tel']     
        try:
            
           client = Client.objects.get(tel=tel)
           
           salle = Reservation_salle.objects.get(client=client)
           print(salle.salle.numero)
           date_s = Reservation_salle.objects.get(client=client)
           print(date_s.date_reservation)
           cl = Reservation_salle.objects.get(client=client)
           print(cl.client.nom)
           idd = salle.id
           reservation = {'tel' : tel,
                        'client' : client,
                        'tel' : tel,                             
                        'salle' : salle,                             
                        'date_s' : date_s,
                        'idd' : idd }
           
           return render (request , 'Reservation/Rechercher_reservation_salle.html',reservation )
          
        except:
            return render (request , 'Reservation/Rechercher_reservation_salle.html', {})
    else:    
        return render (request , 'Reservation/Rechercher_reservation_salle.html', {})
    


#------------------------------------------------recherche reservation table-----------------------------------------



def rechercher_reservation_table(request):
    if request.method=="POST":
        tel = request.POST['tel']     
        try:
            
           client = Client.objects.get(tel=tel)
           
           table = Reservation_table.objects.get(client=client)
           print(table.table.numero)
           date_s = Reservation_table.objects.get(client=client)
           print(date_s.date_reservation)
           cl = Reservation_table.objects.get(client=client)
           print(cl.client.nom)
           idd = table.id
           reservation = {'tel' : tel,
                        'client' : client,
                        'tel' : tel,                             
                        'table' : table,                             
                        'date_s' : date_s,
                        'cl' : 'cl',
                        'idd' : idd }
           
           return render (request , 'Reservation/Rechercher_reservation_table.html',reservation )
          
        except:
            return render (request , 'Reservation/Rechercher_reservation_table.html', {})
    else:    
        return render (request , 'Reservation/Rechercher_reservation_table.html', {})
    


#------------------------------------------------recherche reservation salle table-----------------------------------------



def rechercher_reservation_salle_table(request):
    if request.method=="POST":
        tel = request.POST['tel']     
        try:
            
           client = Client.objects.get(tel=tel)
           print(client.nom)
           if Reservation_salle.objects.get(client=client) and Reservation_table.objects.get(client=client) :
               salle = Reservation_salle.objects.get(client=client) 
               print(salle.salle.numero)
           
               date_salle = Reservation_salle.objects.get(client=client)
               print(date_salle.date_reservation)
           
               cll = Reservation_salle.objects.get(client=client)
               print(cll.client.nom)
               
               table = Reservation_table.objects.get(client=client)
               print(table.table.numero)
           
               date_table = Reservation_table.objects.get(client=client)
               print(date_table.date_reservation)
           
               cl = Reservation_table.objects.get(client=client)
               print(cl.client.nom)
               idd = table.id
               iddd = salle.id
               reservation = {'tel' : tel,
                        'client' : client,
                        'tel' : tel,  
                        'salle' : salle, 
                        'date_salle' : date_salle,   
                        'cll' : cll,                   
                        'table' : table,                             
                        'date_table' : date_table,
                        'cl' : 'cl',
                        'idd' : idd,
                        'iddd' : iddd
                        }
           
               return render (request , 'Reservation/Rechercher_reservation_salle_table.html',reservation )
          
        except:
            return render (request , 'Reservation/Rechercher_reservation_salle_table.html', {})
    else:    
        return render (request , 'Reservation/Rechercher_reservation_salle_table.html', {})
    




#---------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------Fonction impression--------------------------------------------------------------- 
#-------------------------------------------------------------------------------------------------------------------------


#----------------------------------------------------------impression table admin--------------------------


def impression_table_admin(request):
    
    return render (request, 'Reservation/impression_table_admin.html')

#----------------------------------------------------------impression salle admin-------------------------------------

def impression_salle_admin(request,myid):
    reservation = Reservation_salle.object.get(id=myid)
    t = Reservation_salle.object.all()
    return render (request, 'Reservation/impression_salle_admin.html',{'reservation' : reservation},{'t':t})




#---------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------fin----fin-------fin----fin-fin------------------------------------------------------------------------
##-----------------------------------fin fonction partie admin ou agent -----------------------------------## ------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------


############_____________-----------------------PARTIE CLIENT ----------------------------

#---------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------
#########################d------------debut fonction pour partie client ---------------#---------------------------#############
#-----------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------------------------
#-------------------------------------------FONCTION Navbar Client-------------------------------------------
#------------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------Home ----------------------------------------------------


def client_home(request):
    return render(request, 'Reservation/TabledebordClient.html')


#----------------------------------------------------Vos-Rservation----------------------------------------------------


def vos_reservation(request):
    return render(request, 'Reservation/Vos_reservation.html')



#----------------------------------------------------Contactez-Nous-------------------------------------------------------


def contactez_nous(request):
    return render(request, 'Reservation/Contactez_nous.html')


#--#---------------------------------------------------Connecter------------------------------------------------------------



#---------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------FONCTION DE L AJOUT------------------------------------------------------

    
#-------------------------------------------------------------ajout reservation table client ----------------------------------

def ajout_vip_table(request):
    if request.method=="POST":   
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        tel = request.POST['tel']
        email = request.POST['email']
        nombre_place = request.POST['nombre_place']
        type_evenement = request.POST['type_evenement'] 
        iddd = request.POST['idd']
        date_reservation = request.POST['date_reservation']
        try:
                
           table = Table.objects.get(id=iddd)
           
           if date_reservation  != Reservation_table.date_reservation :
              client = Client.objects.create(nom=nom, prenom=prenom, tel=tel, email=email)
              r = Reservation_table.objects.create(client = client, table=table, date_reservation = date_reservation , nombre_place=nombre_place, type_evenement=type_evenement)
              client.save()
              r.save() 
              idd = r.id
              return render(request, 'Reservation/impression_table.html',{'idd': idd}) 
           else:
              return render(request, 'Reservation/Salle.html')  
        except:
            res = {'msg' : 1}
            return render(request, 'Reservation/Salle.html',{'res' : res})
      
    tables = Table.objects.filter(type="VIP")
    return render(request,'Reservation/ajout_reservation_vip.html',{'tables' : tables} )

def ajout_vip_table_admin(request):
    if request.method=="POST":   
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        tel = request.POST['tel']
        email = request.POST['email']
        nombre_place = request.POST['nombre_place']
        type_evenement = request.POST['type_evenement'] 
        iddd = request.POST['idd']
        date_reservation = request.POST['date_reservation']
        try:
                
           table = Table.objects.get(id=iddd)
           
           if date_reservation  != Reservation_table.date_reservation :
              client = Client.objects.create(nom=nom, prenom=prenom, tel=tel, email=email)
              r = Reservation_table.objects.create(client = client, table=table, date_reservation = date_reservation , nombre_place=nombre_place, type_evenement=type_evenement)
              client.save()
              r.save() 
              idd = r.id
              return render(request, 'Reservation/impression_table_admin.html',{'idd': idd}) 
           else:
              return render(request, 'Reservation/Salle.html')  
        except:
            res = {'msg' : 1}
            return render(request, 'Reservation/Salle.html',{'res' : res})
      
    tables = Table.objects.filter(type="VIP")
    return render(request,'Reservation/ajout_reservation_vip_table_admin.html',{'tables' : tables} )

def ajout_normal_table_admin(request):
    if request.method=="POST":   
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        tel = request.POST['tel']
        email = request.POST['email']
        nombre_place = request.POST['nombre_place']
        type_evenement = request.POST['type_evenement'] 
        iddd = request.POST['idd']
        date_reservation = request.POST['date_reservation']
        try:
                
           table = Table.objects.get(id=iddd)
           
           if date_reservation  != Reservation_table.date_reservation :
              client = Client.objects.create(nom=nom, prenom=prenom, tel=tel, email=email)
              r = Reservation_table.objects.create(client = client, table=table, date_reservation = date_reservation , nombre_place=nombre_place, type_evenement=type_evenement)
              client.save()
              r.save() 
              idd = r.id
              return render(request, 'Reservation/impression_table_admin.html',{'idd': idd}) 
           else:
              return render(request, 'Reservation/Table.html')  
        except:
            res = {'msg' : 1}
            return render(request, 'Reservation/Salle.html',{'res' : res})
      
    tables = Table.objects.filter(type="NORMAL")
    return render(request,'Reservation/ajout_reservation_normal_table_admin.html',{'tables' : tables} )




def ajout_vip_salle_admin(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method=="POST":   
            nom = request.POST['nom']
            prenom = request.POST['prenom']
            tel = request.POST['tel']
            email = request.POST['email']
            iddd = request.POST['idd']
            date_reservation = request.POST['date_reservation']
            nombre_table = request.POST['nombre_table']
            type_evenement = request.POST['type_evenement']
            salle = Salle.objects.get(id=iddd)
            client = Client.objects.create(nom=nom, prenom=prenom, tel=tel, email=email)
            r = Reservation_salle.objects.create(client = client, salle=salle, 
                                                    date_reservation = date_reservation,
                                                    nombre_table=nombre_table,
                                                    type_evenement=type_evenement)
            client.save()
            r.save()
            idd = r.id;
            return render (request, 'Reservation/impression_salle_admin.html', {'idd': idd}) 
    
        salles = Salle.objects.filter(type="VIP")
        return render(request, 'Reservation/Ajout_reservation_salle_vip_admin.html',{'salles':salles})

def ajout_normal_salle_admin(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method=="POST":   
            nom = request.POST['nom']
            prenom = request.POST['prenom']
            tel = request.POST['tel']
            email = request.POST['email']
            iddd = request.POST['idd']
            date_reservation = request.POST['date_reservation']
            nombre_table = request.POST['nombre_table']
            type_evenement = request.POST['type_evenement']
            salle = Salle.objects.get(id=iddd)
            client = Client.objects.create(nom=nom, prenom=prenom, tel=tel, email=email)
            r = Reservation_salle.objects.create(client = client, salle=salle, 
                                                    date_reservation = date_reservation,
                                                    nombre_table=nombre_table,
                                                    type_evenement=type_evenement)
            client.save()
            r.save()
            idd = r.id;
            return render (request, 'Reservation/impression_salle_admin.html', {'idd': idd})
         
        # salles_normales = Salle.objects.filter(type="NORMAL")
        # salles_non_reserves = salles_normales.exclude(reservation_salle__isnull=False)
        salles = Salle.objects.filter(type="NORMAL")

        return render(request, 'Reservation/Ajout_reservation_salle_normal_admin.html',{'salles':salles})


def ajout_normal_table(request):
    if request.method=="POST":   
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        tel = request.POST['tel']
        email = request.POST['email']
        nombre_place = request.POST['nombre_place']
        type_evenement = request.POST['type_evenement'] 
        iddd = request.POST['idd']
        date_reservation = request.POST['date_reservation']
        try:
                
           table = Table.objects.get(id=iddd)
           
           if date_reservation  != Reservation_table.date_reservation :
              client = Client.objects.create(nom=nom, prenom=prenom, tel=tel, email=email)
              r = Reservation_table.objects.create(client = client, table=table, date_reservation = date_reservation , nombre_place=nombre_place, type_evenement=type_evenement)
              client.save()
              r.save() 
              idd = r.id
              return render(request, 'Reservation/impression_table.html',{'idd': idd}) 
           else:
              return render(request, 'Reservation/Salle.html')  
        except:
            res = {'msg' : 1}
            return render(request, 'Reservation/Salle.html',{'res' : res})
      
    tables = Table.objects.filter(type="NORMAL")
    return render(request,'Reservation/ajout_reservation_normal.html',{'tables' : tables} )

def ajout_vip_salle(request):
    if request.method=="POST":   
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        tel = request.POST['tel']
        email = request.POST['email']
        iddd = request.POST['idd']
        date_reservation = request.POST['date_reservation']
        nombre_table = request.POST['nombre_table']
        type_evenement = request.POST['type_evenement']
        salle = Salle.objects.get(id=iddd)
        client = Client.objects.create(nom=nom, prenom=prenom, tel=tel, email=email)
        r = Reservation_salle.objects.create(client = client, salle=salle, 
                                             date_reservation = date_reservation,
                                             nombre_table=nombre_table,
                                             type_evenement=type_evenement)
        client.save()
        r.save()
        idd = r.id;
        return render (request, 'Reservation/impression_salle.html', {'idd': idd}) 
    
    salles = Salle.objects.filter(type="VIP")
    return render(request, 'Reservation/ajout_reservation_salle_vip.html',{'salles':salles})

def ajout_normal_salle(request):
    if request.method=="POST":   
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        tel = request.POST['tel']
        email = request.POST['email']
        iddd = request.POST['idd']
        date_reservation = request.POST['date_reservation']
        nombre_table = request.POST['nombre_table']
        type_evenement = request.POST['type_evenement']
        salle = Salle.objects.get(id=iddd)
        client = Client.objects.create(nom=nom, prenom=prenom, tel=tel, email=email)
        r = Reservation_salle.objects.create(client = client, salle=salle,
                                             nombre_table =nombre_table,
                                             date_reservation = date_reservation,
                                             type_evenement = type_evenement
                                             )
        client.save()
        r.save()
        idd = r.id;
        return render (request, 'Reservation/impression_salle.html', {'idd': idd}) 
    salles = Salle.objects.filter(type="NORMAL")
    return render(request, 'Reservation/ajout_reservation_salle_normal.html',{'salles':salles})



def ajout_reservation_table_client(request):
    if request.method=="POST":   
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        tel = request.POST['tel']
        email = request.POST['email']
        nombre_place = request.POST['nombre_place']
        type_evenement = request.POST['type_evenement'] 
        iddd = request.POST['idd']
        date_reservation = request.POST['date_reservation']
        try:
            
           table = Table.objects.get(id=iddd)
           
           if date_reservation  != Reservation_table.date_reservation :
              client = Client.objects.create(nom=nom, prenom=prenom, tel=tel, email=email)
              r = Reservation_table.objects.create(client = client, table=table, date_reservation = date_reservation , nombre_place=nombre_place, type_evenement=type_evenement)
              client.save()
              r.save() 
              idd = r.id
              return render(request, 'Reservation/impression_table.html',{'idd': idd}) 
           else:
              return render(request, 'Reservation/Salle.html')  
        except:
            res = {'msg' : 1}
            return render(request, 'Reservation/Salle.html',{'res' : res})
      
    tables = Table.objects.all()
    return render(request,'Reservation/Ajout_reservation_table_Client.html',{'tables' : tables} )


#-----------------------------------------------------------ajout reservation salle client -------------------------------------------


def ajout_reservation_salle_client(request):
    if request.method=="POST":   
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        tel = request.POST['tel']
        email = request.POST['email']
        iddd = request.POST['idd']
        date_reservation = request.POST['date_reservation']
        salle = Salle.objects.get(id=iddd)
        client = Client.objects.create(nom=nom, prenom=prenom, tel=tel, email=email)
        r = Reservation_salle.objects.create(client = client, salle=salle, date_reservation = date_reservation)
        client.save()
        r.save()
        idd = r.id;
        return render (request, 'Reservation/impression_salle.html', {'idd': idd}) 
    salles = Salle.objects.all()
    return render(request, 'Reservation/Ajout_reservation_salle_Client.html',{'salles':salles})


#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------- FONCTION RESERVATION---------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------Reservation client----------------------------

def reservation_client(request):
    return render(request, 'Reservation/Ajout_Reservation.html')


#------------------------------------------------------------------------vos reservation salle pour "client"-----------------------------------

def vos_reservation_salle(request):
    
    return render(request, 'Reservation/Vos_reservation_salle.html')

#-------------------------------------------------------------------------vos reservation table pour "client"-----------------------------------

def vos_reservation_table(request):
    
    return render(request, 'Reservation/Vos_reservation_table.html')


#------------------------------------------------------------------------vos reservation salle table pour "client"-----------------------------------

def vos_reservation_salle_table(request):
    return render(request, 'Reservation/Vos_reservation_salle_table.html')




#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------- FONCTION RECHERCHE---------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------


#------------------------------------------------------------cherche reservation client qui reserve salle et table en m temp--------------------------


def cherche_reservation_client_salle_table(request):
     if request.method == "POST":
           tel = request.POST['tel']
           reservation = {}
          
           try:
                client = Client.objects.get(tel=tel)  
                print(client.nom) 
                print(client.prenom)
               
                if Reservation_table.objects.get(client=client) and Reservation_salle.objects.get(client=client): 
                    
                    table = Reservation_table.objects.get(client=client)
                    print(table.table.numero)
                    print(table.table.salle.numero)
                    date = Reservation_table.objects.get(client=client)
                    print(date.date_reservation)
                    salle = Reservation_salle.objects.get(client=client)
                    print(salle.salle.numero)
                    date_s = Reservation_salle.objects.get(client=client)
                    print(date_s.date_reservation)
                    
                    id_t = Reservation_table.objects.get(client=client) 
                    id_ta = (id_t.id) 
                    id_s = Reservation_salle.objects.get(client=client) 
                    id_sa = (id_s.id)
                    
                    
                    reservation = {'tel' : tel,
                                'client' : client,
                                'table' : table,                             
                                'date' : date,
                                'salle' : salle,                             
                                'date_s' : date_s,
                                'id_t' : id_t,
                                'id_ta' : id_ta,
                                 'id_s' : id_s,
                                'id_sa' : id_sa,
                                'msg' : 1 }
                     
                    return render(request, 'Reservation/cherche_reservation_client_salle_table.html',reservation)
            
           except:
               reservation = {'msg' : "ne existe pas"}
               return render(request, 'Reservation/cherche_reservation_client_salle_table.html',reservation)
                
           
                
     return render(request, 'Reservation/cherche_reservation_client.html')


#--------------------------------------------------cherche reservation client qui reserve des tables seulement-----------------------------------


def cherche_reservation_client_table(request):
    
     if request.method == "POST":
           tel = request.POST['tel']
           reservation = {}
          
           try:
                client = Client.objects.get(tel=tel)  
                print(client.nom) 
                print(client.prenom)
               
                if Reservation_table.objects.get(client=client) : 

                    table = Reservation_table.objects.get(client=client)
                    
                    print(table.table.numero)
                    print(table.table.salle.numero)
                    date = Reservation_table.objects.get(client=client)
                    print(date.date_reservation)
                    idd = Reservation_table.objects.get(client=client)
                    iddd = idd.id
                    reservation = {'tel' : tel,
                                'client' : client,
                                'table' : table,                             
                                'date' : date,
                                'iddd' : iddd,
                                'msg' : 1}
                     
                    return render(request, 'Reservation/cherche_reservation_client_table.html',reservation)
            
           except:
                  reservation = {'msg' : "ne existe pas"}
                  return render(request, 'Reservation/cherche_reservation_client_table.html',reservation)
    
    
     return render(request, 'Reservation/cherche_reservation_client_table.html')           


#------------------------------------------------cherche reservation client qui reserve des salle-----------------------------


def cherche_reservation_client_salle(request):
    
     if request.method == "POST":
           tel = request.POST['tel']
           reservation = {}
          
           try:
                client = Client.objects.get(tel=tel)  
                print(client.nom) 
                print(client.prenom)
               
                if Reservation_salle.objects.get(client=client) : 

                    salle = Reservation_salle.objects.get(client=client)
                    
                    print(salle.salle.numero)
                    date = Reservation_salle.objects.get(client=client)
                    print(date.date_reservation)
                    idd = Reservation_salle.objects.get(client=client)
                    iddd = (idd.id)
                    
                    reservation = {'tel' : tel,
                                'client' : client,
                                'salle' : salle,                             
                                'date' : date,
                                'idd' : idd,
                                'iddd' : iddd,
                                'msg' : 1}
                     
                    return render(request, 'Reservation/cherche_reservation_client_salle.html',reservation)
            
           except:
                  reservation = {'msg' : "ne existe pas"}
                  return render(request, 'Reservation/cherche_reservation_client_salle.html',reservation)
    
    
     return render(request, 'Reservation/cherche_reservation_client_salle.html')           



#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------FONCTION BILLET OU TICKET--------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------

#---------------------------------------------------fonction billet ou ticket---------- --------------------------

def Billet(request):
     
    return render (request, 'Reservation/Billet.html')

#----------------------------------------------------fonction billet ou ticket du reservation de salle-------------------------------


def Billet_salle(request,myid):
    billet = Reservation_salle.objects.get(id = myid)
    date = datetime.now 
    return render (request, 'Reservation/Billet_salle.html',{'billet':billet,'date':date})

#----------------------------------------------------fonction billet ou ticket du reservation de table-------------------------------


def Billet_table(request,myid):
    billet = Reservation_table.objects.get(id = myid)
    date = datetime.now 
    return render (request, 'Reservation/Billet_table.html',{'billet':billet,'date':date})

#--------------------------------------------fonction billet ou ticket de reservation du table et salle en m temp-------------------------------


def Billet_salle_table(request,myid,mid):
    try:
       if Reservation_salle.objects.get(id=myid) and  Reservation_table.objects.get(id=mid) :
          billet_salle = Reservation_salle.objects.get(id=myid)
          print(billet_salle.client.nom)
          print(billet_salle.client.prenom)
          print(billet_salle.salle.numero)
          date = datetime.now 
          billet_table = Reservation_table.objects.get(id=mid)
          print(billet_table.table.numero)
          context = {'billet_salle' : billet_salle,
                     'date' : date,
                     'billet_table' : billet_table
                    }
          return render (request, 'Reservation/Billet_salle_table.html',context)
       return render (request, 'Reservation/Billet_salle_table.html',context)
    
    except:
        return render (request, 'Reservation/Billet_salle_table.html',{})
 

#----------------------------------------------------Avant impression ticket salle ! --------------------------------------------

def impression_salle(request):
    
    return render (request, 'Reservation/impression_salle.html')

#-----------------------------------------------------Avant impression ticket table !--------------------------------------------------------


def impression_table(request):
    
    return render (request, 'Reservation/impression_table.html')


       




