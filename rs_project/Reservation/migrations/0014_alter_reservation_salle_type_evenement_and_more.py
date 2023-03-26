# Generated by Django 4.1.7 on 2023-03-26 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reservation', '0013_alter_reservation_table_nombre_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation_salle',
            name='type_evenement',
            field=models.CharField(choices=[('diner_vip', 'diner_vip'), ('diner_Normal', 'diner_Normal'), ('Conference', 'Conference'), ('Festival', 'Festival'), ('Mariage', 'Mariage'), ('autre', 'autre')], default='autre', max_length=50),
        ),
        migrations.AlterField(
            model_name='reservation_table',
            name='type_evenement',
            field=models.CharField(choices=[('diner_vip', 'diner_vip'), ('diner_Normal', 'diner_Normal'), ('Conference', 'Conference'), ('Festival', 'Festival'), ('Mariage', 'Mariage'), ('autre', 'autre')], default='autre', max_length=50),
        ),
    ]
