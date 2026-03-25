from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from infrastructure.config import app_settings
from infrastructure.container import init_container
from infrastructure.web.api.api_v1.api import api_router
from starlette.responses import RedirectResponse

container = init_container()

app = FastAPI(
    title=app_settings.PROJECT_NAME,
    openapi_url=f"{app_settings.API_V1_STR}/openapi.json",
)
app.include_router(api_router, prefix=app_settings.API_V1_STR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=app_settings.APP_CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index(request: Request):
    return RedirectResponse(url="/docs")


container.wire(packages=["infrastructure.web.api", "common", __name__])
