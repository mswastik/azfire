from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/reg")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/clf")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/clt")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/fc")
async def index(request: Request):
    return templates.TemplateResponse("fc.html", {"request": request})

@app.post("/fc")
async def index(request: Request):
    item = await request.form()
    print(item.items())
    return item