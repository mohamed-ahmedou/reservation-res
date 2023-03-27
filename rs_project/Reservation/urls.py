
from django.contrib.auth import views as authViews
from . import views
from django.urls import path

#-------------------------------------------------------------Login----------------------------------------------------------------------------
    
 

urlpatterns = [
    #nouveau--------------
    path('choix_table/', views.choix_table, name="choix_table"),
    path('choix_salle/', views.choix_salle, name="choix_salle"),
    path('ajout_vip_table/', views.ajout_vip_table, name="ajout_vip_table"),
    path('ajout_normal_table/', views.ajout_normal_table, name="ajout_normal_table"),
    
    path('ajout_vip_salle/', views.ajout_vip_salle, name="ajout_vip_salle"),
    path('ajout_normal_salle/', views.ajout_normal_salle, name="ajout_normal_salle"),
    # admin
    path('choix_salle_admin/', views.choix_salle_admin, name="choix_salle_admin"),
    path('choix_table_admin/', views.choix_table_admin, name="choix_table_admin"),
    path('ajout_vip_salle_admin/', views.ajout_vip_salle_admin, name="ajout_vip_salle_admin"),
    path('ajout_normal_salle_admin/', views.ajout_normal_salle_admin, name="ajout_normal_salle_admin"),
    path('ajout_vip_table_admin/', views.ajout_vip_table_admin, name="ajout_vip_table_admin"),
    path('ajout_normal_table_admin/', views.ajout_normal_table_admin, name="ajout_normal_table_admin"),
    
    
    #nouveau ----------------------------

    path('login/' ,views.userLogin, name="login"),
    path('register/' ,views.register, name="register"),
#-------------------------------------------------------------urls Navbar----------------------------------------------------------
    path('',views.client_home, name="client_home"),
    path('home/',views.home,name="home"),
    
    path('reservation/',views.reservation, name="reservation"),
    path('reservation_salle/',views.reservation_salle, name="reservation_salle"),
    path('reservation_table/',views.reservation_table, name="reservation_table"),
    
    path('salle/',views.salle,name="salle"),
    path('table/',views.table, name="table"),
    path('client/',views.client, name="client"),
   
   
   
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------urls L'ajout----------------------------------------------------------

    
    path('ajout_reservation_salle/', views.ajout_reservation_salle, name="ajout_reservation_salle"),
    
    path('ajout_reservation_table/', views.ajout_reservation_table, name="ajout_reservation_table"),
    
    path('ajout_salle/',views.ajout_salle, name="ajout_salle"),
    
    path('ajout_table/',views.ajout_table, name="ajout_table"),
    
    path('ajout_client/', views.ajout_client, name="ajout_client"), 
    
    
   #-------------------------------------------------------------urls modification----------------------------------------------------------

  
    
    path('modifier_reservation_salle/<int:myid>/',views.modifier_reservation_salle, name="modifier_reservation_salle"),
    
    # reste ici fonction modifier_reservation_table !!
    
    path('modifier_salle/<int:myid>/', views.modifier_salle, name="modifier_salle"),
    
    path('modifier_table/<int:myid>/', views.modifier_table, name="modifier_table"),
    
    path('modifier_client/<int:myid>/', views.modifier_client, name="modifier_client"),
    
    
#---------------------------------------------------------suppression------------------------------------------------------------------
    
   
    path('supprimer_reservation_salle/<int:myid>/', views.supprimer_reservation_salle, name="supprimer_reservation_salle"),
    
    path('supprimer_reservation_table/<int:myid>/', views.supprimer_reservation_table, name="supprimer_reservation_table"),
    
    path('supprimer_reservation_salle_table/<int:myid>/<int:mid>/', views.supprimer_reservation_salle_table, name="supprimer_reservation_salle_table"),
    
    path('supprimer_salle/<int:myid>/', views.supprimer_salle, name="supprimer_salle"),
    
    path('supprimer_table/<int:myid>/', views.supprimer_table, name="supprimer_table"),
    
    path('supprimer_client/<int:myid>/', views.supprimer_client, name="supprimer_client"),
    


##--------------------------------------------------------------Urls Navbar client-----------------------------------------------------------------

##-------------------------------------------------------------- Home -----------------------------------------------------------------
    
    path('',views.client_home, name="client_home"),
    path('reservation_client/',views.reservation_client, name="reservation_client"),
    
##------------------------------------------------------------Vos-Reservation-----------------------------------------------------------------
 ##------------------------------------------------------------Vos-Reservation-----------------------------------------------------------------
   
    path('vos_reservation/', views.vos_reservation, name="vos_reservation"),
    path('vos_reservation_salle/',views.vos_reservation_salle, name="vos_reservation_salle"),
    path('vos_reservation_table/',views.vos_reservation_table, name="vos_reservation_table"),
    path('vos_reservation_salle_table/',views.vos_reservation_salle_table, name="vos_reservation_salle_table"),
    
      
    
  ##-----------------------------------------------------Recherche pour partie client----------------------------------------------------------------------
   
    
    path('cherche_reservation_client_salle/', views.cherche_reservation_client_salle, name="cherche_reservation_client_salle"),
    path('cherche_reservation_client_table/', views.cherche_reservation_client_table, name="cherche_reservation_client_table"),
    path('cherche_reservation_client_salle_table/',views.cherche_reservation_client_salle_table, name="cherche_reservation_client_salle_table"),
      
##------------------------------------------------------------Contactez-Nous-----------------------------------------------------------------
    
    path('contactez_nous/',views.contactez_nous, name="contactez_nous"),
    
##-----------------------------------------------------------------------------------------------------------------------------------------
##-----------------------------------------------------L urls ajout pour partie client----------------------------------------------------------------------
    
    path('ajout_reservation_salle_client/',views.ajout_reservation_salle_client, name="ajout_reservation_salle_client"),
    path('ajout_reservation_table_client/',views.ajout_reservation_table_client, name="ajout_reservation_table_client"),
  #------------------------------------------------------Recherche--------------------------------------------------------------------------------------------------------
  
  
    path('rechercher_reservation_salle/',views.rechercher_reservation_salle, name="rechercher_reservation_salle"),
    
    path('rechercher_reservation_table/',views.rechercher_reservation_table, name="rechercher_reservation_table"),
    
    path('rechercher_reservation_salle_table/',views.rechercher_reservation_salle_table, name="rechercher_reservation_salle_table"),

    
    path('rechercher_salle/', views.rechercher_salle, name="rechercher_salle"), 
    
    path('rechercher_table/', views.rechercher_table, name="rechercher_table"),
    
    path('rechercher_client/', views.rechercher_client, name="rechercher_client"), 
   
   ##-----------------------------------------------------impression pour partie client----------------------------------------------------------------------
   
    path('impression_table/',views.impression_table, name="impression_table"),
    path('impression_salle/',views.impression_salle, name="impression_salle"),


##------------------------------------------------------Billet ou ticket partie client------------------------------------------

    path('Billet/', views.Billet, name="Billet"),
    path('Billet_salle/<int:myid>/', views.Billet_salle, name="Billet_salle"),
    path('Billet_table/<int:myid>/', views.Billet_table, name="Billet_table"),
    path('Billet_salle_table/<int:myid>/<int:mid>/', views.Billet_salle_table, name="Billet_salle_table"),
    
    
   
   


]