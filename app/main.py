from fastapi import FastAPI
from starlette.responses import HTMLResponse
from app.api.auth import router as auth_router
from app.api.admin_panel import router as admin_panel_router
from app.api.mock_views import router as mock_views_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(admin_panel_router)
app.include_router(mock_views_router)


@app.get("/", response_class=HTMLResponse)
async def welcome():
    return (
        "<h2> Добро Пожаловать</h2>\n"
        "<p><a href=http://127.0.0.1:8000/docs>Перейти в документацию </a></p>\n"
    )
