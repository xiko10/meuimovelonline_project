from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    # Rota para processar a solicitação de reserva para uma unidade específica
    path('solicitar/<int:unidade_id>/', views.solicitar_reserva_view, name='solicitar_reserva'),
    path('reservar-direto/<int:unidade_id>/', views.reserva_direta_corretor_view, name='reserva_direta_corretor'),
]