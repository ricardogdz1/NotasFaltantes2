from django.urls import path
from . import views

app_name = 'analisador'

urlpatterns = [
    path('', views.pagina_inicial, name='index'),
    path('processar/', views.processar_arquivo, name='processar'),
    path(
        "ads.txt",
        TemplateView.as_view(template_name="ads.txt", content_type="text/plain"),
        name="ads-txt",
    ),
]
