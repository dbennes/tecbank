# Generated by Django 3.2.5 on 2021-07-26 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='conta_usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('cpf', models.CharField(max_length=200)),
                ('identidade', models.CharField(max_length=200)),
                ('agencia', models.IntegerField()),
                ('conta', models.IntegerField()),
                ('digito_conta', models.IntegerField()),
                ('email', models.CharField(max_length=200)),
                ('numero_celular', models.CharField(max_length=200)),
                ('endereco', models.CharField(max_length=200)),
                ('cidade', models.CharField(max_length=200)),
                ('estado', models.CharField(max_length=200)),
                ('pais', models.CharField(max_length=200)),
                ('saldo_brl', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
    ]
