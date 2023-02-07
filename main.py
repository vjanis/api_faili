import uvicorn
import os
from fastapi import FastAPI, File, UploadFile
from kods.logosana import logi, auditacija
from config import CHUNK_SIZE, FAILU_FOLDERIS, FILE_SIZE
from datetime import datetime, date

app = FastAPI()

FILE_FOLDER = os.path.join('.', FAILU_FOLDERIS)

@app.get("/")
async def root():
    return {"message": "failu savākšana strādā"}


# curl -F "file=@sezona.csv" http://localhost:8000/uploadfile
@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        if file is not None:
            if len(await file.read()) >= FILE_SIZE:
                auditacija(darbiba='api_faili_web', parametri="Augšuplādētais fails par lielu: " + file.filename,
                           autorizacijas_lvl='WARNING', statuss='OK')
                logi("Augšuplādētais fails par lielu: " + file.filename)
                return {"Augšuplādētais fails par lielu: " + file.filename}
            if file.filename[-4:] == '.csv':
                jauns_nosaukums = file.filename[:-4] + "_" + \
                                  datetime.utcnow().strftime('%Y%m%d_%H%M%S%f')[:-3] + file.filename[:-4]
                fullpath = os.path.join(FILE_FOLDER, jauns_nosaukums)
                await chunked_copy(file, fullpath)
                auditacija(darbiba='api_faili_web', parametri="fails augšuplādēts: " + fullpath,
                           autorizacijas_lvl='INFO', statuss='OK')
                logi("fails augšuplādēts: " + fullpath)
                return {"fails augšuplādēts: ": fullpath}
            else:
                auditacija(darbiba='api_faili_web', parametri="nekorekts faila tips: " + file.filename,
                           autorizacijas_lvl='WARNING', statuss='OK')
                logi("nekorekts faila tips: " + file.filename)
                return {"nekorekts faila tips: ": file.filename}
        else:
            auditacija(darbiba='api_faili_web', parametri="nav augšuplādējamā faila ",
                       autorizacijas_lvl='WARNING', statuss='OK')
            logi("nav augšuplādējamā faila ")
            return {"nav augšuplādējamā faila "}
    except Exception as e:
        auditacija(darbiba='api_faili_web', parametri="fails augšuplāde neveiksmiga: " + str(e),
                   autorizacijas_lvl='ERROR', statuss='OK')
        logi("fails augšuplāde neveiksmiga: " + str(e))
        return {"fails augšuplāde neveiksmiga: ": str(e)}


async def chunked_copy(src, dst):
    try:
        await src.seek(0)
        with open(dst, "wb") as buffer:
            while True:
                contents = await src.read(CHUNK_SIZE)
                if not contents:
                    print(f"Src completely consumed\n")
                    break
                print(f"Consumed {len(contents)} bytes from Src file\n")
                buffer.write(contents)
    except Exception as e:
        print("asdasdasd: "+str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
