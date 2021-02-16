from fastapi import FastAPI, File, Security, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyQuery, APIKey
from starlette.status import HTTP_403_FORBIDDEN
from classdetection import ClassDetection
from fastapi.responses import JSONResponse
import uvicorn


app = FastAPI()
detection = ClassDetection()
app.add_middleware(CORSMiddleware, allow_origins=[
                   '*'], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)


async def get_api_key(api_key_query: str = Security(APIKeyQuery(name='key', auto_error=False))):
    if api_key_query == 'protected_ai':
        return api_key_query
    else:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN,
                            detail="Could not validate credentials")


@app.post("/objects/")
async def drawing(file: bytes = File(...), api_key: APIKey = Depends(get_api_key)):
    return JSONResponse(content=detection.prediction(file))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
