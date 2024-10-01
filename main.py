from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import polars as pl
import pickle

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/reg")
async def index(request: Request):
    return templates.TemplateResponse("reg.html", {"request": request})

@app.get("/clf")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/clt")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/fc")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/reg")
async def index(request: Request):
    item = await request.form()
    #print(item.items())
    def predf(item):
        dft=pl.DataFrame([[item.get('day'), item.get('month'), item.get('year'), item.get('season'), item.get('holiday'), item.get('weekday'), item.get('workingday'),
                        item.get('weathersit'), item.get('temp'), item.get('atemp'), item.get('hum'), item.get('windspeed')]],schema=['day', 'mnth', 'year', 'season', 'holiday', 'weekday', 'workingday',
                        'weathersit', 'temp', 'atemp', 'hum', 'windspeed'])
        with open('bike.pkl', 'rb') as f:
            reg=pickle.load(f)   
        return reg.predict(dft)        
    p=predf(item)
    return HTMLResponse('<div class="text-md p-5 bg-gray-300 rounded-md" id="result">The predicted no. of rentals are {}</div>'.format(int(p[0])))

@app.get("/contact")
async def index(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})