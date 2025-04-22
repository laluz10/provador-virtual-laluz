from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import uuid
import os
import json

app = FastAPI(title="Provador Virtual Laluz", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Backend do provador virtual rodando 🎯"}

@app.post("/upload-user-photo/")
async def upload_user_photo(file: UploadFile = File(...)):
    filename = f"user_{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"user_image": filename}

@app.post("/upload-jewel-photo/")
async def upload_jewel_photo(file: UploadFile = File(...)):
    filename = f"jewel_{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"jewel_image": filename}

class TryOnRequest(BaseModel):
    user_image: str
    jewel_image: str
    category: str

@app.post("/generate-tryon/")
def generate_tryon(data: TryOnRequest):
    tryon_filename = f"tryon_{uuid.uuid4().hex}.png"
    tryon_url = f"https://laluz-provador.onrender.com/fake/{tryon_filename}"  # simulado
    return {
        "image_generated": tryon_url,
        "message": f"😍 Que linda combinação! Enviamos para o WhatsApp 📲 34997083781"
    }

@app.get("/categories/")
def list_categories():
    return ["brincos", "colares", "pulseiras", "argolas", "conjuntos", "chockers"]

class Lead(BaseModel):
    nome: str
    telefone: str
    peca: str
    imagem_gerada: str

@app.post("/save-lead/")
def save_lead(data: Lead):
    lead_data = data.dict()
    lead_data["contato_fixo"] = "34997083781"

    with open("leads.json", "a") as f:
        f.write(json.dumps(lead_data) + "\n")

    return {"status": "Lead salvo com sucesso", "whatsapp": "34997083781"}
