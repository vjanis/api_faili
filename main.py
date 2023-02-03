import uvicorn
import os
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

FAILU_MAPE = os.path.join('.', 'faili')
ATLAUTIE_FAILI = set(['csv'])
CHUNK_SIZE = 2 ** 20  # 1MB

@app.get("/")
async def root():
    return {"message": "api_web darbojas"}

#curl -F "file=@sezona.csv" http://localhost:8000/uploadfile
@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    fullpath = os.path.join(FAILU_MAPE, file.filename)
    await chunked_copy(file, fullpath)
    return {"File saved to disk at": fullpath}

async def chunked_copy(src, dst):
    await src.seek(0)
    with open(dst, "wb") as buffer:
        while True:
            contents = await src.read(CHUNK_SIZE)
            if not contents:
                print(f"Src completely consumed\n")
                break
            print(f"Consumed {len(contents)} bytes from Src file\n")
            buffer.write(contents)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
