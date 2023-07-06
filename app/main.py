from fastapi import FastAPI, File, UploadFile
import io

from models.classifier import video_to_frames, classify_frames


app = FastAPI()


@app.get("/")
async def healthcheck():
    return "I am alive!"

'''@app.post("/classify")
async def classify(video: UploadFile = File(...)):
    try:
        print(f"file name: {video.filename}")
        print(f"file type: {video.content_type}")
        contents = await video.read()
        file_like_object = io.BytesIO(contents)
        frames = video_to_frames(file_like_object)
        results = classify_frames(frames)
        return results
    except Exception as e:
        return str(e)
'''

'''
@app.post("/classify")
async def classify(video: UploadFile = File(...)):
    print(f"file name: {video.filename}")  # should print 'video.mp4'
    print(f"file type: {video.content_type}")  # should print 'application/octet-stream'
    with open(video.filename, 'wb+') as f:
        f.write(await video.read())  # save the uploaded file to a new file
    frames = video_to_frames(video.filename)
    results = classify_frames(frames)
    return results
'''


@app.post("/classify")
async def classify(video: UploadFile = File(...)):
    contents = await video.read()
    file_like_object = io.BytesIO(contents)
    frames = video_to_frames(file_like_object)
    results = classify_frames(frames)
    return results


'''
@app.post("/classify")
async def classify(video: UploadFile = File(...)):
    # Read the file in-memory, but it should not be a problem unless the video file is very large
    contents = await video.read()
    file_like_object = io.BytesIO(contents)

    # Преобразуем видео в кадры
    frames = video_to_frames(file_like_object)
    
    # Классифицируем кадры
    predictions = classify_frames(frames)
    
    # Возвращаем предсказания в виде строки
    return ' '.join(predictions)
'''
