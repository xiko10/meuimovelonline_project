# Generated by Django 5.2.3 on 2025-06-17 21:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('empreendimentos', '0003_filtrolocalizacao_programahabitacional_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='empreendimento',
            name='corretores_autorizados',
            field=models.ManyToManyField(blank=True, related_name='empreendimentos_autorizados_corretor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='empreendimento',
            name='imobiliarias_autorizadas',
            field=models.ManyToManyField(blank=True, related_name='empreendimentos_autorizados_imob', to='core.imobiliaria'),
        ),
        migrations.AddField(
            model_name='empreendimento',
            name='venda_todas_imobiliarias',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='empreendimento',
            name='venda_todos_corretores_autonomos',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='empreendimento',
            name='visivel_consumidor_final',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='empreendimento',
            name='visivel_para_nao_autorizados',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='FluxoPagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serie', models.CharField(help_text="Ex: 'Ato', '30 dias', '60 dias', 'Anual 2025'", max_length=100)),
                ('quantidade', models.PositiveIntegerField(help_text='Número de parcelas nesta série')),
                ('valor_unitario', models.DecimalField(decimal_places=2, help_text='Valor de cada parcela', max_digits=15)),
                ('empreendimento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fluxo_pagamento', to='empreendimentos.empreendimento')),
            ],
        ),
    ]
