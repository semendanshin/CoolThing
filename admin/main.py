import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes import (dashboard_router, bots_router, bot_router, fallback_router, chats_router,
                    campaigns_router, gpt_settings_router, auth_router)

from middlewares import check_for_auth

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

app.middleware('http')(check_for_auth)

app.include_router(dashboard_router)
app.include_router(bots_router)
app.include_router(bot_router)
app.include_router(fallback_router)
# app.include_router(prompts_router)
app.include_router(chats_router)
app.include_router(campaigns_router)
app.include_router(gpt_settings_router)
app.include_router(auth_router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
