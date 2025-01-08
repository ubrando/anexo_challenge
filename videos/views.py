from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import cv2
import os
from datetime import datetime

def upload_video(request):
    face_images = []
    if request.method == 'POST' and request.FILES['video']:
        video_file = request.FILES['video']
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'videos'))
        filename = fs.save(video_file.name, video_file)
        file_url = fs.url(filename)

        # Verifique se o arquivo foi realmente salvo
        print(f"Arquivo de vídeo salvo em: {video_file.name}")

        # Processar o vídeo após o upload
        video_path = os.path.join(settings.MEDIA_ROOT, 'videos', filename)
        print(f"Path do vídeo para processamento: {video_path}")
        face_images = process_video(video_path)  # Processa o vídeo e extrai as faces

        if face_images:
            print(f"Faces detectadas: {face_images}")
        else:
            print("Nenhuma face detectada.")

        return render(request, 'videos/upload.html', {'file_url': file_url, 'face_images': face_images})

    return render(request, 'videos/upload.html')


def process_video(video_path):
    face_images = []
    # Processamento com OpenCV
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Erro ao abrir o vídeo: {video_path}")
        return face_images  # Se não conseguir abrir o vídeo, retorna lista vazia
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Verificar se a pasta de faces existe
    faces_dir = os.path.join(settings.MEDIA_ROOT, 'faces')
    if not os.path.exists(faces_dir):
        os.makedirs(faces_dir)  # Cria a pasta caso ela não exista
    
    face_count = 0
    fps = cap.get(cv2.CAP_PROP_FPS)  # Obtém os frames por segundo do vídeo
    frame_interval = int(fps * 3)  # Aqui, processamos a cada 1 segundo (pode ajustar o intervalo)
    frame_count = 0  # Contador de frames

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Processa apenas a cada `frame_interval` frames
        if frame_count % frame_interval == 0:
            # Convertendo para escala de cinza
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detectando faces com parâmetros ajustados
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )

            for (x, y, w, h) in faces:
                # Recortando a face
                face = frame[y:y+h, x:x+w]
                face_filename = f"face_{datetime.now().strftime('%Y%m%d%H%M%S')}_{face_count}.jpg"
                face_path = os.path.join(faces_dir, face_filename)
                cv2.imwrite(face_path, face)
                face_images.append(f"/media/faces/{face_filename}")
                face_count += 1

        frame_count += 1

    cap.release()
    return face_images
