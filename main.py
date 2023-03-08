import uvicorn
import os
import secrets
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status
from kods.logosana import logi, auditacijas
from config import CHUNK_SIZE, FAILU_FOLDERIS, FILE_SIZE
from datetime import datetime
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from config import AUGSUPLADE_LIETOTAJS, AUGSUPLADE_PAROLE


app = FastAPI()

security = HTTPBasic()

FILE_FOLDER = os.path.join('.', FAILU_FOLDERIS)

@app.get("/")
async def root():
    return {"message": "failu savākšana strādā"}

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = bytes(AUGSUPLADE_LIETOTAJS, 'utf-8')
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = bytes(AUGSUPLADE_PAROLE, 'utf-8')
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        try:
            auditacijas(darbiba='api_faili_web', parametri="Nekorekts augšuplādes lietotājvārds vai parole",
                        autorizacijas_lvl='WARNING', statuss='OK', metrika=27)
            logi("Nekorekts augšuplādes lietotājvārds vai parole")
        except:
            logi("ERROR auditacija: Nekorekts augšuplādes lietotājvārds vai parole")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nekorets lietotājvārds vai parole",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# curl -F "file=@sezona.csv" http://localhost:8000/uploadfile
@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...), username: str = Depends(get_current_username)):
    try:
        if file is not None:
            if len(await file.read()) >= FILE_SIZE:
                auditacijas(darbiba='api_faili_web', parametri="Augšuplādētais fails par lielu: " + file.filename,
                           autorizacijas_lvl='WARNING', statuss='OK', metrika=6)
                logi("Augšuplādētais fails par lielu: " + file.filename)
                return {"Augšuplādētais fails par lielu: " + file.filename}
            if file.filename[-4:] == '.csv':
                jauns_nosaukums = datetime.utcnow().strftime('%Y%m%d_%H%M%S%f')[:-3] + "_" + file.filename
                fullpath = os.path.join(FILE_FOLDER, jauns_nosaukums)
                await chunked_copy(file, fullpath)
                auditacijas(darbiba='api_faili_web', parametri="fails augšuplādēts: " + fullpath,
                           autorizacijas_lvl='INFO', statuss='OK', metrika=8)
                logi("fails augšuplādēts: " + fullpath)
                return {"fails augšuplādēts: ": fullpath}
            else:
                auditacijas(darbiba='api_faili_web', parametri="nekorekts faila tips: " + file.filename,
                           autorizacijas_lvl='WARNING', statuss='OK', metrika=7)
                logi("nekorekts faila tips: " + file.filename)
                return {"nekorekts faila tips: ": file.filename}
        else:
            auditacijas(darbiba='api_faili_web', parametri="nav augšuplādējamā faila ",
                       autorizacijas_lvl='WARNING', statuss='OK', metrika=9)
            logi("nav augšuplādējamā faila ")
            return {"nav augšuplādējamā faila "}
    except Exception as e:
        auditacijas(darbiba='api_faili_web', parametri="fails augšuplāde neveiksmiga: " + str(e),
                   autorizacijas_lvl='ERROR', statuss='OK', metrika=9)
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
