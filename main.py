from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import polars as pl
import pickle
from urllib.request import urlopen

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
        #with open('bike.pkl', 'rb') as f:
        #with open(urlopen('https://firstml.blob.core.windows.net/first/bike.pkl'),'rb') as f:
        reg=pickle.load(urlopen('https://firstml.blob.core.windows.net/first/bike.pkl'))   
        return reg.predict(dft)        
    p=predf(item)
    return HTMLResponse('''<div class="text-md text-center p-5 bg-gray-300 rounded-md" id="result">The predicted no. of rentals are &nbsp; 
                        <b class="text-2xl text-blue-700">{}</b></div>
                        <div role="status" id="spin" class="hidden w-8 h-8inline-block rounded-full border-4 border-solid border-e-transparent animate-spin fill-blue-600 border-blue-600 motion-reduce:animate-[spin_1.5s_linear_infinite]">
      <span class="text-transparent">...</span>'''.format(int(p[0])))

@app.get("/contact")
async def index(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})