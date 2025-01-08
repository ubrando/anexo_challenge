# models.py

from django.db import models

class Video(models.Model):
    file = models.FileField(upload_to="videos/", help_text="Arquivo de vídeo no formato MP4")
    uploaded_at = models.DateTimeField(auto_now_add=True, help_text="Data de upload do vídeo")

    def __str__(self):
        return f"Video uploaded at {self.uploaded_at}"
