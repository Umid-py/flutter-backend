from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="My Flutter Backend API")

# Ma'lumotlarni saqlaydigan global o'zgaruvchi
users_db = [
    {"id": 1, "name": "Ali", "age": 25, "city": "Toshkent"},
    {"id": 2, "name": "Vali", "age": 30, "city": "Samarqand"},
    {"id": 3, "name": "Sobir", "age": 28, "city": "Buxoro"}
]

# Keyingi ID
next_id = 4

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "Salom! Backend muvaffaqiyatli ishlamoqda 🚀",
        "status": "success"
    }

@app.get("/api/users")
def get_users():
    return {"success": True, "users": users_db}

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    for user in users_db:
        if user['id'] == user_id:
            return {"success": True, "user": user}
    return {"success": False, "message": "Foydalanuvchi topilmadi"}

@app.post("/api/users")
def create_user(name: str = Form(...), age: int = Form(...)):
    global next_id
    
    # Yangi foydalanuvchi yaratish
    new_user = {
        "id": next_id,
        "name": name,
        "age": age,
        "city": "Toshkent"
    }
    
    # Ro'yxatga qo'shish
    users_db.append(new_user)
    next_id += 1
    
    print(f"Yangi foydalanuvchi qo'shildi: {new_user}")
    print(f"Jami foydalanuvchilar: {len(users_db)}")
    
    return {
        "success": True,
        "message": "Foydalanuvchi yaratildi",
        "user": new_user
    }

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int):
    global users_db
    
    for i, user in enumerate(users_db):
        if user['id'] == user_id:
            deleted_user = users_db.pop(i)
            print(f"O'chirildi: {deleted_user}")
            return {
                "success": True,
                "message": "Foydalanuvchi o'chirildi",
                "user": deleted_user
            }
    
    return {"success": False, "message": "Foydalanuvchi topilmadi"}
@app.put("/api/users/{user_id}")
def update_user(user_id: int, name: str = Form(...), age: int = Form(...)):
    global users_db
    
    for user in users_db:
        if user['id'] == user_id:
            user['name'] = name
            user['age'] = age
            print(f"Yangilandi: {user}")
            return {
                "success": True,
                "message": "Foydalanuvchi yangilandi",
                "user": user
            }
    
    return {"success": False, "message": "Foydalanuvchi topilmadi"}