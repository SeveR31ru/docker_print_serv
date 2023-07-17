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
    printers=config["COMMON"]["printers"].split(',')
    printers_port=config["COMMON"]["printers_ports"].split(',')
except:
    print("Ошибка настроек")
    exit()

description = """
Апи для сервера наклеек нашей компании

**Для Артема- Swagger перемещен в "/"**

# Описание методов

Имеется три способа печати наклеек:

* **Печать таблицей**

* **Печать текстом**

* **Печать датаматрикса**

# Что нужно знать перед печатью

## Поля в json

Для использование каждой функции можно нажать на неё и кнопку try it out.
Откроется окно с json файлом, который нужно заполнить данными по шаблону и нажать EXECUTE.

Поля данных:
1. Text- что вы хотите внести. Пишите сплошным текстом нужную вам информацию, **КРОМЕ** таблиц. Для таблиц отдельное пояснение ниже.
2. Fontsize- размер шрифта, ставите на свое усмотрение.
3. На каком принтере печатать(смотрите пояснение ниже).



## Принтеры

* 0-маленький принтер 20х30мм, предпочтителен для печати датаматриксов
* 1-большой принтер 55х60(около того), предпочтителен для таблиц и текста

Можно использовать их не по назначению, но крайне не рекомендуется

## Особенности json для таблицы

**КРАЙНЕ ВАЖНО**, чтобы в text был массив массивов

Для обывателя- в каждых [] скобках должна быть одна строка элементов, разделенных запятыми и взятыми в кавычки. После полного 
написания строки вы закрываете скобку, ставите запятую после открываете новые скобки и пишете аналогично там. За последней скобкой
запятая не ставится.Пример:

[["Первая","Строка","Таблицы"],["Вторая","Строка","Таблицы"],["Третья","Строка","Таблицы"]]

Columns заполняется в виде просто массива, т.е отдельными словами в кавычкам через запятую. Пример: 

["что вам надо 1","что вам надо 2","что вам надо 3"]

Пример правильного json-а:
{ 
  "text": [
    [
      "1","2","3",
    ],
    [
    "4","5","6"
    ]
  ],
  "columns": [
    "k1","k2","k3"
  ],
  "fontsize": 150,
  "printer": 100
}

## Если что-то не работает

Для непродвинутых:

1. Перезагрузить моноблок
2. Проверить подключение принтеров. **ВАЖНО** тыкнуть их в те же слоты, в которых они были до вытыкивания
3. Напечатать что угодно по разу на каждом принтере

Для продвинутых:

1. Глянуть статус контейнера и логи на моноблоке в docker 
2. Пофиксить на свое усмотрение
"""

app = FastAPI(description=description,docs_url="/",redoc_url="/docs")

class Text(BaseModel):
    text:str
    fontsize:Union[int,None]=100
    printer:int

class Table(BaseModel):
    text:list[list]
    columns:list
    fontsize:Union[int,None]=100
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
