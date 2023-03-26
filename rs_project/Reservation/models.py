from unicodedata import category
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
# Create your models here.
from django.core.validators import MaxValueValidator, MinValueValidator

class Client(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    verification = RegexValidator(regex="[1-9]{8}", message="Veuillez entrer un numero correct")
    phone_validator = RegexValidator(regex=r'^(1[1-9]|2[1-2,4,7,8]|3[1-5]|3[7-8]|4[1-9]'
                                       r'|5[1,3-5]|6[1-9]|7[1,3,4,5,7,9]'
                                       r'|8[1-9]|9[1-9]){1}[0-9]{8,9}$',
                                 message="entrer un nombre valide")
    tel = models.IntegerField(validators=[phone_validator])
  
    
    
    def __str__(self):
        return f" {self.nom} {self.prenom}"

class Salle(models.Model):
    SALLE_TYPE = (
        ('VIP', 'vip'),
        ('NORMAL', 'Normal')
    )
    numero = models.IntegerField()
    type = models.CharField(max_length=50, choices=SALLE_TYPE)
    
    
    def __str__(self):
      return f"le numero de salle est :{self.numero}  et le type : {self.type}"
    

class Table(models.Model):
    TABLE_TYPE = (
        ('VIP', 'vip'),
        ('NORMAL', 'Normal')
    )
    numero = models.IntegerField()
    type = models.CharField(max_length=50, choices=TABLE_TYPE)
    salle = models.ForeignKey(Salle, null=True, on_delete=models.CASCADE)
    disponiblité = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.numero} {self.type}"
    
class Reservation_table(models.Model):
    Evenement_TYPE_table = (
        ('diner_vip', 'diner_vip'),
        ('diner_Normal', 'diner_Normal'),
        ('Conference', 'Conference'),
        ('Festival', 'Festival'),
        ('Mariage', 'Mariage'),
        ('autre', 'autre')
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    table = models.ForeignKey(Table,  on_delete=models.CASCADE)
    date_reservation = models.DateTimeField()
    disponiblité = models.BooleanField(default=True)
    nombre_place = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)],default=1)
    type_evenement = models.CharField(max_length=50, choices=Evenement_TYPE_table)
    
    
    def __str__(self):
       return f"{self.client.nom} {self.client.prenom} a reserver la table numero {self.table.numero} dans la salle numero {self.table.salle.numero}, date de reservation: {self.date_reservation}"
  
class Reservation_salle(models.Model):
    Evenement_TYPE_salle = (
        ('diner_vip', 'diner_vip'),
        ('diner_Normal', 'diner_Normal'),
        ('Conference', 'Conference'),
        ('Festival', 'Festival'),
        ('Mariage', 'Mariage'),
        ('autre', 'autre')

    )
    client = models.ForeignKey(Client,  on_delete=models.CASCADE)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    nombre_place = models.IntegerField
    date_reservation = models.DateTimeField()
    nombre_table = models.IntegerField(default=10)
    type_evenement = models.CharField(max_length=50, choices=Evenement_TYPE_salle)
    
    def __str__(self):
            return f"{self.client.nom} {self.client.prenom} a reserver la salle numero {self.salle.numero}, date de reservation: {self.date_reservation}"
    
      