# Generated by Django 3.2.5 on 2021-07-31 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0005_alter_perfil_saldo_brl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='conta',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]