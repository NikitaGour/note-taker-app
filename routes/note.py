from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from config.db import conn

note = APIRouter(prefix="/notes")
templates = Jinja2Templates(directory="templates")


@note.get("/", response_class=HTMLResponse)
def read_item(request: Request):
    docs = conn.fastapidb.fastapicoll.find()
    newdoc = []

    for i in docs:
        newdoc.append({
            "id": str(i["_id"]),
            "title": i.get("title"),
            "desc": i.get("desc"),
            "important": i.get("important", False),
        })

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "newdoc": newdoc}
    )


@note.post("/")
async def create_item(request: Request):
    form = await request.form()

    print(form)  # DEBUG – you should see values here

    conn.fastapidb.fastapicoll.insert_one({
        "title": form.get("title"),
        "desc": form.get("desc"),
        "important": bool(form.get("important"))
    })

    return RedirectResponse("/notes", status_code=303)
