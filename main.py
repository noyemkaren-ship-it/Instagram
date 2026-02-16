from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import CRUD_user
import CRUD_image
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


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
    existing_user = CRUD_user.get_user_by_name(name)
    if existing_user:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Пользователь с таким именем уже существует"}
        )

    # Получаем следующий ID
    all_users = CRUD_user.get_all_users()
    new_id = 1
    if all_users:
        new_id = max(user['id'] for user in all_users) + 1

    # Добавляем пользователя
    CRUD_user.add_user(new_id, name, password)

    # Перенаправляем на логин
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
    if CRUD_user.check_user(name, password):
        # Успешный вход - перенаправляем в Instagram
        return RedirectResponse(url="/instagram", status_code=303)
    else:
        # Неправильный логин или пароль
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Неверное имя пользователя или пароль"}
        )


@app.get("/instagram")
async def instagram_page(request: Request):
    """Главная страница с фото"""
    # Получаем все изображения из базы
    all_images = CRUD_image.get_all_images()

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

@app.get("/add-test-photos")
async def add_test_photos():

    girls_photos = [
        "https://avatars.mds.yandex.net/i?id=683fb4d010ed7d35995eb28c79f1a372_l-4575625-images-thumbs&n=13",
        "https://i.pinimg.com/736x/f1/a9/b3/f1a9b33d70b95b7b888813e2ad0dd1a6.jpg",
        "https://i.pinimg.com/736x/ea/63/80/ea6380c15a9babc6aee5aff33559fcf6.jpg",
        "https://i.pinimg.com/736x/05/35/63/053563dcaffb06fd611c8e18e2681107.jpg"
    ]

    memes_photos = [
        "https://i.pinimg.com/736x/4b/7c/48/4b7c485dc75a7ea0162fed25296cc605.jpg",
        "https://i.pinimg.com/736x/d9/3d/b5/d93db54c17e8602aed3717e7caa253c9.jpg",
        "https://i.pinimg.com/736x/36/c8/39/36c839615879b4bfd7102abde3757040.jpg",
        "https://i.pinimg.com/736x/d3/2d/36/d32d3652b4194be31286c3d74d0c480f.jpg"
    ]

    for i, url in enumerate(girls_photos):
        img_id = i + 1
        CRUD_image.add_image(img_id, url, 1)

    for i, url in enumerate(memes_photos):
        img_id = i + 100
        CRUD_image.add_image(img_id, url, 2)

    return {"message": f"Добавлено {len(girls_photos)} фото девочек и {len(memes_photos)} мемов"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=7000, reload=True)