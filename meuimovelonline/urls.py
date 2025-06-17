from django.contrib import admin
from django.urls import path, include # Garanta que 'include' está importado
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Rota do admin nativo
    path('superadmin/', admin.site.urls), 
    
    # ADICIONE/MODIFIQUE ESTA LINHA para incluir as rotas do painel
    path('painel/', include('painel.urls')),
    
    # Rota principal que inclui as urls do app 'core' (home, login, etc.)
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)