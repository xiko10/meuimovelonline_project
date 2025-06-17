# core/management/commands/seed_data.py

from django.core.management.base import BaseCommand
from django.utils.text import slugify
import random
from core.models import User, Imobiliaria
from empreendimentos.models import Empreendimento, Unidade

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de teste para desenvolvimento.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando o povoamento do banco de dados...")

        # --- ATENÇÃO: Limpando dados existentes (exceto superusuários) ---
        self.stdout.write("Limpando dados antigos...")
        Unidade.objects.all().delete()
        Empreendimento.objects.all().delete()
        Imobiliaria.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        
        # --- Criando Usuários para cada Perfil ---
        self.stdout.write("Criando usuários de teste...")

        # 1. Anunciante
        anunciante_user = User.objects.create_user(
            username='anunciante_teste',
            password='123',
            first_name='João',
            last_name='Construtor',
            email='anunciante@teste.com',
            perfil='anunciante'
        )

        # 2. Imobiliária e seu Admin
        imobiliaria_a = Imobiliaria.objects.create(nome='Imobiliária Alfa', cnpj='11.111.111/0001-11', status='ativa')
        
        admin_imob_user = User.objects.create_user(
            username='admin_imob_teste',
            password='123',
            first_name='Maria',
            last_name='Gestora',
            email='admin.imob@teste.com',
            perfil='admin_imob',
            imobiliaria=imobiliaria_a
        )

        # 3. Gerente e Corretores da Imobiliária Alfa
        gerente_user = User.objects.create_user(
            username='gerente_teste', password='123', first_name='Carlos', last_name='Líder',
            email='gerente@teste.com', perfil='gerente', imobiliaria=imobiliaria_a
        )
        corretor1_user = User.objects.create_user(
            username='corretor1_teste', password='123', first_name='Ana', last_name='Vendedora',
            email='corretor1@teste.com', perfil='corretor', imobiliaria=imobiliaria_a
        )
        corretor2_user = User.objects.create_user(
            username='corretor2_teste', password='123', first_name='Pedro', last_name='Negociador',
            email='corretor2@teste.com', perfil='corretor', imobiliaria=imobiliaria_a
        )
        
        self.stdout.write("\n--- Dados de Login ---")
        self.stdout.write("Anunciante: anunciante_teste / 123")
        self.stdout.write("Admin Imob: admin_imob_teste / 123")
        self.stdout.write("Gerente:    gerente_teste / 123")
        self.stdout.write("Corretor 1: corretor1_teste / 123")
        self.stdout.write("Corretor 2: corretor2_teste / 123")
        self.stdout.write("----------------------\n")


        # --- Criando Empreendimentos e Unidades ---
        self.stdout.write("Criando empreendimentos e unidades...")

        # Empreendimento 1
        emp1 = Empreendimento.objects.create(
            nome="Residencial Vista do Parque",
            slug=slugify("Residencial Vista do Parque"),
            anunciante_responsavel=anunciante_user,
            status_publicacao='publicado',
            # ... preencha outros campos obrigatórios com valores de teste
            tipo_empreendimento='vertical', uso='residencial', status_empreendimento='lancamento',
            descricao_curta='More ao lado do parque com a melhor vista da cidade.',
            cep='01000-000', endereco_completo='Praça da Sé, 100', numero_whatsapp_atendimento='11987654321'
        )
        for i in range(10):
            Unidade.objects.create(
                empreendimento=emp1,
                tipo='apartamento',
                metragem=random.uniform(50.0, 85.5),
                quartos=random.choice([2, 3]),
                banheiros=random.choice([1, 2]),
                vagas=random.choice([1, 2]),
                valor_total=random.uniform(350000, 600000),
                status='disponivel' if random.random() > 0.3 else 'reservada'
            )

        # Empreendimento 2
        emp2 = Empreendimento.objects.create(
            nome="Torres do Sol Nascente",
            slug=slugify("Torres do Sol Nascente"),
            anunciante_responsavel=anunciante_user,
            status_publicacao='publicado',
            # ... preencha outros campos obrigatórios
            tipo_empreendimento='vertical', uso='residencial', status_empreendimento='em_obras',
            descricao_curta='Modernidade e conforto no coração do bairro.',
            cep='02000-000', endereco_completo='Av. Principal, 2000', numero_whatsapp_atendimento='11987654321'
        )
        for i in range(5):
            Unidade.objects.create(
                empreendimento=emp2, tipo='studio', metragem=random.uniform(25.0, 40.0),
                quartos=1, banheiros=1, vagas=random.choice([0, 1]),
                valor_total=random.uniform(250000, 400000), status='disponivel'
            )
        
        self.stdout.write(self.style.SUCCESS('Banco de dados populado com sucesso!'))