from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI(title="English-Uzbek Dictionary API")

# So'zlar bazasi
words_db = [
    {"id": 1, "english": "hello", "uzbek": "salom", "example": "Hello, how are you?"},
    {"id": 2, "english": "book", "uzbek": "kitob", "example": "I'm reading a book."},
    {"id": 3, "english": "water", "uzbek": "suv", "example": "Drink some water."}
]

next_id = 4

# YANGI: Oxirgi foydalanuvchilar
recent_users = []

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
        "message": "Dictionary API ishlayapti 📚",
        "status": "success"
    }

# YANGI: Foydalanuvchi kirganini ro'yxatga olish
@app.post("/api/login")
def user_login(name: str = Form(...)):
    login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Oxirgi kirishlardan topish (agar avval kirgan bo'lsa)
    existing = None
    for user in recent_users:
        if user['name'].lower() == name.lower():
            existing = user
            break
    
    if existing:
        # Vaqtni yangilash
        existing['last_login'] = login_time
        existing['visit_count'] += 1
    else:
        # Yangi foydalanuvchi
        new_user = {
            "name": name,
            "last_login": login_time,
            "visit_count": 1
        }
        recent_users.insert(0, new_user)  # Boshiga qo'shish
    
    # Faqat oxirgi 10 tani saqlash
    if len(recent_users) > 10:
        recent_users.pop()
    
    print(f"Login: {name} at {login_time}")
    
    return {
        "success": True,
        "message": f"Xush kelibsiz, {name}!",
        "user": {"name": name, "last_login": login_time}
    }

# YANGI: Oxirgi kirishlarni olish
@app.get("/api/recent-users")
def get_recent_users():
    return {
        "success": True,
        "users": recent_users[:10]  # Oxirgi 10 ta
    }

# So'zlar endpointlari (oldingicha)
@app.get("/api/words")
def get_words():
    return {"success": True, "words": words_db}

@app.get("/api/words/{word_id}")
def get_word(word_id: int):
    for word in words_db:
        if word['id'] == word_id:
            return {"success": True, "word": word}
    return {"success": False, "message": "So'z topilmadi"}

@app.post("/api/words")
def create_word(english: str = Form(...), uzbek: str = Form(...), example: str = Form(...)):
    global next_id
    
    new_word = {
        "id": next_id,
        "english": english.lower(),
        "uzbek": uzbek,
        "example": example
    }
    
    words_db.append(new_word)
    next_id += 1
    
    print(f"Yangi so'z qo'shildi: {new_word}")
    
    return {
        "success": True,
        "message": "So'z qo'shildi",
        "word": new_word
    }

@app.put("/api/words/{word_id}")
def update_word(word_id: int, english: str = Form(...), uzbek: str = Form(...), example: str = Form(...)):
    for word in words_db:
        if word['id'] == word_id:
            word['english'] = english.lower()
            word['uzbek'] = uzbek
            word['example'] = example
            print(f"Yangilandi: {word}")
            return {
                "success": True,
                "message": "So'z yangilandi",
                "word": word
            }
    
    return {"success": False, "message": "So'z topilmadi"}

@app.delete("/api/words/{word_id}")
def delete_word(word_id: int):
    for i, word in enumerate(words_db):
        if word['id'] == word_id:
            deleted_word = words_db.pop(i)
            print(f"O'chirildi: {deleted_word}")
            return {
                "success": True,
                "message": "So'z o'chirildi",
                "word": deleted_word
            }
    
    return {"success": False, "message": "So'z topilmadi"}