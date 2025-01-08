from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('upload/', views.upload_video, name='upload_video'),  # URL para fazer upload de vídeo
    path('processar-video/', views.process_video, name='process_video'),  # URL para processar o vídeo
]

# Configuração para servir arquivos de mídia no modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
