import os
import uuid
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from rembg import remove, new_session
from PIL import Image

# optimization
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

app = FastAPI(title="Background Remover API")

session = new_session()

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"status": "API is running"}


@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):

    file_id = str(uuid.uuid4())

    input_path = f"{OUTPUT_DIR}/{file_id}.png"
    output_path = f"{OUTPUT_DIR}/output_{file_id}.png"

    # save uploaded file
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # process image
    image = Image.open(input_path)
    output = remove(image, session=session)

    output.save(output_path)

    return FileResponse(output_path, media_type="image/png")