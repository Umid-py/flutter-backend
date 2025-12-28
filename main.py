from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="English-Uzbek Dictionary API")

# Ma'lumotlar
words_db = [
    {"id": 1, "english": "hello", "uzbek": "salom", "example": "Hello, how are you?"},
    {"id": 2, "english": "book", "uzbek": "kitob", "example": "I'm reading a book."},
    {"id": 3, "english": "water", "uzbek": "suv", "example": "Drink some water."}
]

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
        "message": "Dictionary API ishlayapti 📚",
        "status": "success"
    }

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
    print(f"Jami so'zlar: {len(words_db)}")
    
    return {
        "success": True,
        "message": "So'z qo'shildi",
        "word": new_word
    }

@app.put("/api/words/{word_id}")
def update_word(word_id: int, english: str = Form(...), uzbek: str = Form(...), example: str = Form(...)):
    global words_db
    
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
    global words_db
    
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