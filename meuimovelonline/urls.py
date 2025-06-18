# meuimovelonline/urls.py (VERSÃO FINAL E CORRIGIDA)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('painel/', include('painel.urls')),
    path('empreendimentos/', include('empreendimentos.urls', namespace='empreendimentos')),
    path('reservas/', include('reservas.urls', namespace='reservas')),
    path('', include('core.urls')),
]

# --- BLOCO DE CÓDIGO CRÍTICO ADICIONADO AQUI ---
# Esta configuração só funciona em modo de DEBUG (desenvolvimento) e é essencial
# para que o servidor de desenvolvimento do Django possa servir os arquivos.
if settings.DEBUG:
    # Adiciona a rota para servir arquivos estáticos (CSS, JS, etc.)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Adiciona a rota para servir arquivos de mídia (uploads dos usuários)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)