from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
import os
#import uuid
import easyocr

app = FastAPI()

db = []

model = easyocr.Reader(['en', 'ar'])


@app.post("/images/")
async def create_upload_file(file: UploadFile = File(...)):

    # file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()  # <-- Important!

    print(file.filename)

    db.append(contents)

    result = model.readtext(file.filename)
    height = 0
    maxH = 0
    dictOfHeights = {}
    for word in result:
        height = int(word[0][3][1]) - int(word[0][0][1])
        dictOfHeights[word[1]] = height
        maxH = max(maxH, height)
    # print(maxH)
    for k, v in dictOfHeights.items():
        if v == maxH:
            return k