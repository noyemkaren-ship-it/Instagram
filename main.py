from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import db_operations as db
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# ========== СТРАНИЦЫ ==========

@app.get("/")
async def register_page(request: Request):
    """Страница регистрации"""
    return templates.TemplateResponse(
        "register.html",
        {"request": request, "error": None}
    )


@app.post("/register")
async def register_user(
        request: Request,
        name: str = Form(...),
        password: str = Form(...)
):
    """Обработка регистрации"""
    # Проверяем, есть ли уже такой пользователь
    existing_user = db.get_user_by_name(name)
    if existing_user:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Пользователь с таким именем уже существует"}
        )

    # Добавляем пользователя
    db.add_user(name, password)

    return RedirectResponse(url="/login", status_code=303)


@app.get("/login")
async def login_page(request: Request):
    """Страница входа"""
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": None}
    )


@app.post("/login")
async def login_user(
        request: Request,
        name: str = Form(...),
        password: str = Form(...)
):
    """Обработка входа"""
    if db.check_user(name, password):
        return RedirectResponse(url="/instagram", status_code=303)
    else:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Неверное имя пользователя или пароль"}
        )


@app.get("/instagram")
async def instagram_page(request: Request):
    """Главная страница с фото"""
    # Получаем все изображения из базы
    all_images = db.get_all_images()

    # Разделяем по категориям
    girls_images = [img for img in all_images if img['category'] == 1]
    memes_images = [img for img in all_images if img['category'] == 2]

    return templates.TemplateResponse(
        "instagram.html",
        {
            "request": request,
            "girls_images": girls_images,
            "memes_images": memes_images,
            "all_images": all_images
        }
    )


# ========== ДОБАВЛЕНИЕ ТЕСТОВЫХ ФОТО ==========

@app.get("/add-test-photos")
async def add_test_photos():
    """Добавить тестовые фото"""

    # Фото девочек (категория 1)
    girls_photos = [
        "https://avatars.mds.yandex.net/i?id=683fb4d010ed7d35995eb28c79f1a372_l-4575625-images-thumbs&n=13",
        "https://i.pinimg.com/736x/f1/a9/b3/f1a9b33d70b95b7b888813e2ad0dd1a6.jpg",
        "https://i.pinimg.com/736x/ea/63/80/ea6380c15a9babc6aee5aff33559fcf6.jpg",
        "https://i.pinimg.com/736x/05/35/63/053563dcaffb06fd611c8e18e2681107.jpg",
        "https://i.pinimg.com/736x/e8/52/b6/e852b6f08a56ab47a259747f5e6c0264.jpg"
    ]

    # Фото мемов (категория 2)
    memes_photos = [
        "https://i.pinimg.com/736x/4b/7c/48/4b7c485dc75a7ea0162fed25296cc605.jpg",
        "https://i.pinimg.com/736x/d9/3d/b5/d93db54c17e8602aed3717e7caa253c9.jpg",
        "https://i.pinimg.com/736x/36/c8/39/36c839615879b4bfd7102abde3757040.jpg",
        "https://i.pinimg.com/736x/d3/2d/36/d32d3652b4194be31286c3d74d0c480f.jpg"
    ]

    # Добавляем фото
    for url in girls_photos:
        db.add_image(url, 1)

    for url in memes_photos:
        db.add_image(url, 2)

    return {"message": f"Добавлено {len(girls_photos)} фото девочек и {len(memes_photos)} мемов"}


@app.get("/db-info")
async def db_info():
    """Информация о базе данных"""
    from simple_db import DB_PATH
    import os

    users = db.get_all_users()
    images = db.get_all_images()

    return {
        "db_path": DB_PATH,
        "db_exists": os.path.exists(DB_PATH),
        "users_count": len(users),
        "images_count": len(images),
        "users": users,
        "images": images
    }


if __name__ == "__main__":
    print("🚀 Запуск сервера...")
    print(f"📁 База данных: ~/instagram_app/instagram.db")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)