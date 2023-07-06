from PIL import Image
import numpy as np
from facenet_pytorch import MTCNN

# Создаем объект MTCNN
detector = MTCNN()

def detect_faces(image):
    # Обнаруживаем лица на изображении
    boxes, _ = detector.detect(image)

    # Создаем список для хранения обнаруженных лиц
    faces = []

    # Проверяем, обнаружены ли лица
    if boxes is not None:
        # Перебираем все обнаруженные лица
        for box in boxes:
            # Получаем координаты лица
            x1, y1, x2, y2 = box

            # Извлекаем лицо
            face = image[int(y1):int(y2), int(x1):int(x2)]

            # Добавляем лицо в список
            faces.append(face)

    # Возвращаем список обнаруженных лиц
    return faces
