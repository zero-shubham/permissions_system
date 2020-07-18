from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
import asyncio
import uvicorn
import os
import sqlalchemy
from application import app, ps
from api.api_v1.api import api_router
from core.config import ORIGINS
from utils.app_event_funcs import shutdown, startup

app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS", "PUT", "DELETE"],
    allow_headers=[
        "Accept",
        "Accept-Encoding",
        "Authorization",
        "Content-Type",
        "Origin",
        "User-Agent"
    ]
)
# api_router.include_router(
#     auth_sys.router,
#     tags=["authentication"]
# )
# api_router.include_router(
#     ps.router
# )
app.include_router(api_router)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run("application:app", host="0.0.0.0",
                port=port, log_level="info", loop="asyncio", reload=True)
