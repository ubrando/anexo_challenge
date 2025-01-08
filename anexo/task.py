from anexo.celery import app

@app.task
def test_task():
    return "Celery is working!"
