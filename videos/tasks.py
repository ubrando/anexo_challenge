# videos/tasks.py
from celery import shared_task
import time

@shared_task
def long_running_task():
    time.sleep(10)  # Simula uma tarefa demorada
    print("Tarefa concluída!")
    return "Tarefa concluída com sucesso!"
