from fastapi import FastAPI, Request, Body, HTTPException, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Union
import uvicorn
import configparser
import print as pr


try:
    config=configparser.ConfigParser()
    config.read("./settings.ini")
    host = str(config["COMMON"]["host"])
    port = int(config["COMMON"]["port"])
    printers=config["COMMON"]["printers"]
    printers_port=config["COMMON"]["printers_ports"]
except:
    print("Ошибка настроек")
    exit()

app = FastAPI()

class Text(BaseModel):
    text:str
    fontsize:Union[int,None]=None
    printer:int

class Table(BaseModel):
    text:list[list]
    columns:list
    fontsize:Union[int,None]=None
    printer:int
class Datamatrix(BaseModel):
    data:str
    printer:int


#POST-запросы
@app.post("/print_table")
def print_table(table:Table):
    try:
        columns=table.columns
        text=table.text
    except:
        return "Ошибка при чтении Json"
    try:
        font_size=table.fontsize
        pr.table_print(columns,text,printers[table.printer],printers_port[table.printer],font_size)
    except:
        pr.table_print(columns,text,printers[table.printer],printers_port[table.printer])
    return "Наклейка ушла в печать"

@app.post("/print_text")
def print_text(message:Text):
    try:
        text=message.text
    except:
        return "Ошибка при чтении Json"
    try:
        font_size=message.fontsize
        pr.text_print(text,printers[message.printer],printers_port[message.printer],font_size)
    except:
        pr.text_print(text,printers[message.printer],printers_port[message.printer])
    return"Наклейка ушла в печать"

@app.post("/print_datamatrix")
def print_datamatrix(datamatrix_info:Datamatrix):
    try:
        pr.datamatrix_print(datamatrix_info.data,printers[datamatrix_info.printer],printers_port[datamatrix_info.printer])
    except:
        return "Ошибка при выполнении функции"
    return "Наклейка ушла в печать"


uvicorn.run(app, host=host, port=port)