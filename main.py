from typing import Union

from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
conn=MongoClient("mongodb://localhost:27017/fastapidb.fastapicoll")



app = FastAPI()
app.mount("/static",StaticFiles(directory="static"),name="static")
templates=Jinja2Templates(directory="templates")

@app.get("/",response_class=HTMLResponse)
def read_item(request:Request):
    doc= conn.fastapidb.fastapicoll.find()
    newdoc=[]
    for i in doc:
        newdoc.append({
           "id": str(i["_id"]),
            "note":i["note"]
        })

    print(f"the db item is :{doc}")
    return templates.TemplateResponse("index.html",{"request":request,"newdoc":newdoc})
#this is a template context, “Make these variables available inside index.html”

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}