import torch
from torchvision import transforms
from PIL import Image
import imageio.v3 as iio
from efficientnet_pytorch import EfficientNet
from collections import Counter


from utils.face_detector import detect_faces


model = EfficientNet.from_name('efficientnet-b7')  # Создаем модель
num_ftrs = model._fc.in_features  # Получаем количество входных признаков в последний слой
model._fc = torch.nn.Linear(num_ftrs, 7)  # Заменяем последний слой на новый, имеющий нужное количество выходов
model.load_state_dict(torch.load('models/EffNetB7_finetuned.pth'))  # Загружаем веса модели
model.eval()  # Переводим модель в режим оценки


# Определение трансформации
transform = transforms.Compose([
    transforms.Resize((48, 48)),
    transforms.Grayscale(num_output_channels=3),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))  # normalize to [-1, 1] for each channel
])


def video_to_frames(video_file):    
    
    frames = []

    for frame in iio.imiter(video_file, plugin="pyav"):
        #frame_bgr = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
        frames.append(frame)
        
    return frames


# Классы эмоций
classes = ['anger', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise'] 


def classify_frames(frames):
    frame_count = len(frames)  # количество кадров
    face_detected_count = 0  # количество кадров, на которых обнаружено лицо
    results = []

    for i, frame in enumerate(frames):
        faces = detect_faces(frame)

        if faces:
            face_detected_count += 1
            face = faces[0]
            tensor = transform(Image.fromarray(face)).unsqueeze(0)
            
            with torch.no_grad():
                output = model(tensor)
                _, predicted = torch.max(output, 1)
                # Получаем вероятности для всех эмоций
                probabilities = torch.nn.functional.softmax(output, dim=1)[0].tolist()
        
            # Добавляем предсказание и другую информацию в список
            results.append({
                'frame': i,
                'emotion': classes[predicted.item()],
                'emotion_probabilities': {classes[j]: probabilities[j] for j in range(len(classes))},
                'faces_detected': len(faces)
            })

    # подсчет количества каждого класса эмоций
    emotion_counter = Counter([result['emotion'] for result in results])

    # общая информация
    summary = {
        "frame_count": frame_count, 
        "face_detected_count": face_detected_count,
        "emotion_statistics": dict(emotion_counter),
    }

    return {"summary": summary, "detailed_results": results}
