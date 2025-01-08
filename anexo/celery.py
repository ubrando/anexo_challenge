from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery import shared_task

# Define o ambiente do Django para o Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')

# Cria a instância do Celery
app = Celery('meuprojeto')

# Usa o namespace 'CELERY' para configurações do Celery no settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carrega automaticamente as tarefas em todos os módulos de tarefas (tasks.py)
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@shared_task
def test_task():
    return "Celery is working!"