from django.urls import path
from . import views

app_name = 'analisador'

urlpatterns = [
    path('', views.pagina_inicial, name='index'),
    path('processar/', views.processar_arquivo, name='processar'),
]