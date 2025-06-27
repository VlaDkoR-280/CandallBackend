from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from src.config import bot_token
from src.telegram import validate_telegram_data
from src.db_handler.database import get_groups_of_user
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

class initDataPost(BaseModel):
    initData: str



@app.post('/api/validate')
async def post_validate(body: initDataPost):
    init_data = await validate_telegram_data(body.initData, bot_token)
    if init_data == None:
        raise HTTPException(status_code=401, detail="Invalid Telegram initData")
    user_id = init_data.user.id
    return {"user_id": user_id}

@app.post('/api/groups')
async def post_groups(body: initDataPost):
    init_data = await validate_telegram_data(body.initData, bot_token)
    if init_data == None:
        raise HTTPException(status_code=401, detail="Invalid Telegram initData")
    user_id = init_data.user.id
    groups = await get_groups_of_user(str(user_id))
    return {'user_id': user_id, 'groups': groups}

if __name__ == '__main__':
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        # reload=True # Debug
    )