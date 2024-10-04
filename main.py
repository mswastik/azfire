from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import polars as pl
import pickle
from urllib.request import urlopen
from statsforecast import StatsForecast
from statsforecast.models import (AutoARIMA,HoltWinters,DynamicOptimizedTheta as DOT)
from statsforecast.utils import AirPassengersDF
import os

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
    return templates.TemplateResponse("fc.html", {"request": request})

@app.post("/reg")
async def index(request: Request):
    item = await request.form()
    def predf(item):
        dft=pl.DataFrame([[item.get('day'), item.get('month'), item.get('year'), item.get('season'), item.get('holiday'), item.get('weekday'), item.get('workingday'),
                        item.get('weathersit'), item.get('temp'), item.get('atemp'), item.get('hum'), item.get('windspeed')]],schema=['day', 'mnth', 'year', 'season', 'holiday', 'weekday', 'workingday',
                        'weathersit', 'temp', 'atemp', 'hum', 'windspeed'])
        reg=pickle.load(urlopen('https://firstml.blob.core.windows.net/first/bike.pkl'))   
        return reg.predict(dft)        
    p=predf(item)
    return HTMLResponse('''<div class="text-md text-center p-5 bg-gray-300 rounded-md" id="result">The predicted no. of rentals are &nbsp; 
                        <b class="text-2xl text-blue-700">{}</b></div>
                        <div role="status" id="spin" class="hidden w-8 h-8inline-block rounded-full border-4 border-solid border-e-transparent animate-spin fill-blue-600 border-blue-600 motion-reduce:animate-[spin_1.5s_linear_infinite]">
      <span class="text-transparent">...</span>'''.format(int(p[0])))

@app.post("/fc")
async def index(request: Request):
    item = await request.form()
    os.environ['NIXTLA_ID_AS_COL'] = '1'
    print(item.get('ar'))
    print(item.get('hw'))
    def predf(item):
        models=[]
        if item.get('ar')=='on':
            models=[AutoARIMA(season_length=int(item.get('season')),stepwise=True,max_p=int(item.get('max_p')),max_q=int(item.get('max_q')))]
        if item.get('hw')=='on':
            models.append(HoltWinters(season_length=int(item.get('season'))))
        if item.get('dto')=='on':
            models.append(DOT(int(item.get('season'))))
            #models = [AutoARIMA(season_length=int(item.get('season')),stepwise=True,max_p=int(item.get('max_p')),max_q=int(item.get('max_q'))),HoltWinters(season_length=int(item.get('season'))),DOT(int(item.get('season')))]
        df = AirPassengersDF
        sf = StatsForecast(models = models,freq = item.get('freq'), n_jobs=-1)
        sf.fit(df)
        forecasts_df = sf.predict(h=int(item.get('fh')))
        fig=sf.plot(df,forecasts_df,engine='plotly')
        fig.update_layout(height=370,width=990)
        return fig.to_html(full_html=False)      
    p=predf(item)
    return HTMLResponse('''<div class="text-md text-center p-5 rounded-md" id="result" style="width:990px;height:370px"><p>Here's how the forecast looks like </p>
                        {}</div>
                        <div role="status" id="spin" class="hidden w-8 h-8inline-block rounded-full border-4 border-solid border-e-transparent animate-spin fill-blue-600 border-blue-600 motion-reduce:animate-[spin_1.5s_linear_infinite]">
      <span class="text-transparent">...</span>'''.format(p))

@app.get("/contact")
async def index(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})