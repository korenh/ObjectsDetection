from fastapi import FastAPI, File, Security, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyQuery, APIKey
from starlette.status import HTTP_403_FORBIDDEN
from classdetection import ClassDetection
from fastapi.responses import JSONResponse
import uvicorn
import config

config = config.get_config()
app = FastAPI(title=config['APP_NAME'], version=config["APP_VERSION"])
detection = ClassDetection()
app.add_middleware(CORSMiddleware, allow_origins=[
                   '*'], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)


async def get_api_key(api_key_query: str = Security(APIKeyQuery(name='key', auto_error=False))):
    if api_key_query == config['APP_SECRET']:
        return api_key_query
    else:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN,
                            detail=config['APP_ERR_MSG'])


@app.post("/objects/")
async def drawing(file: bytes = File(...), api_key: APIKey = Depends(get_api_key)):
    return JSONResponse(content=detection.prediction(file))


if __name__ == "__main__":
    uvicorn.run(app, host=config["APP_HOST"], port=config["APP_PORT"])
