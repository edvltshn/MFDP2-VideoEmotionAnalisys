import streamlit as st
import requests
import os
from PIL import Image
import io

# Добавить заголовок
st.title('My First Data Project 2')

# Заголовок приложения
st.title('Анализ эмоций на видео')

# Адрес сервера для обработки видео
url = 'http://host.docker.internal:8000/classify'

# Вводимый пользователем файл
uploaded_file = st.file_uploader("Загрузите видео урока", type=['mp4'])

if uploaded_file is not None:
    st.write('Файл успешно загружен. Нажмите "Анализировать" для начала обработки.')
    
    # При нажатии кнопки "Анализировать" отправляем видео на сервер для обработки
    if st.button('Анализировать'):
        files = {'video': ('video.mp4', uploaded_file.read(), 'application/octet-stream')}
        response = requests.post(url, files=files)

        if response.status_code == 200:
            st.write('Анализ завершен. Результаты:')
            results = response.json()

            summary = results['summary']
            st.write(f'Количество кадров: {summary["frame_count"]}')
            st.write(f'Количество обнаруженных лиц: {summary["face_detected_count"]}')
            st.write('Статистика эмоций:')
            for emotion, count in summary['emotion_statistics'].items():
                st.write(f'{emotion}: {count}')

        else:
            st.write('Произошла ошибка при обработке видео.')
            st.write(response.text)

