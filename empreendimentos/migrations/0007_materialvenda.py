# Generated by Django 5.2.3 on 2025-06-18 19:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('empreendimentos', '0006_parceria'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialVenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('arquivo', models.FileField(upload_to='materiais_venda/')),
                ('data_upload', models.DateTimeField(auto_now_add=True)),
                ('imobiliaria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materiais', to='core.imobiliaria')),
            ],
            options={
                'verbose_name': 'Material de Venda',
                'verbose_name_plural': 'Materiais de Venda',
                'ordering': ['-data_upload'],
            },
        ),
    ]
