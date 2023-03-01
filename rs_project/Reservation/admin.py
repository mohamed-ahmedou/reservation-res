
from django.contrib import admin
from .models import *

class client (admin.ModelAdmin):
    affichage = ('nom','prenom','tel')
    
class salle(admin.ModelAdmin):
    affichage = ('categorie')
    
class table(admin.ModelAdmin):
    affichage = ('categroie')

class res_table(admin.ModelAdmin):
    affichage = ('table')
    
class res_salle(admin.ModelAdmin):
    affichage = ('salle')

# Register your models here.

admin.site.register(Client)
admin.site.register(Salle)
admin.site.register(Table)
admin.site.register(Reservation_salle)
admin.site.register(Reservation_table)