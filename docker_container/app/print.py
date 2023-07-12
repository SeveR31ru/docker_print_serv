import treepoem
import os
import textwrap
import time
from PIL import Image, ImageDraw, ImageFont
SIZE=(2000,2000)
X_INDEND=100
Y_INDEND=150

def datamatrix_print(datamatrix_data: str,name:str,port:str):
    '''
    Функция для преобразования строки в датаматрикс с названием {строка}.png
    аргументы:
    @damamatrix_data-передаваемая строчка для закодирования её в датаматрикс
    '''
    image = treepoem.generate_barcode(barcode_type="datamatrix",
                                      data=datamatrix_data)  
    image.convert("1").resize((int(SIZE[0]*0.6),int(SIZE[1]*0.6))).save(f"barcode.jpg")
    image_full=Image.new('RGB',SIZE,(255, 255, 255))
    image_text=Image.new('RGB',SIZE,(255, 255, 255))
    image_barcode=Image.open(f"barcode.jpg")
    font=ImageFont.truetype("./Roboto-Black.ttf",180)
    drawer=ImageDraw.Draw(image_text)
    y_point=(SIZE[1]*0.7)
    drawer.text((int(SIZE[0]*0.33), y_point),f"BOARD ID:", font=font, fill='black')
    y_point+=int(SIZE[1]*0.07)
    for line in textwrap.wrap(datamatrix_data,width=18):
        drawer.text((X_INDEND, y_point),line, font=font, fill='black')
        y_point+=int(SIZE[1]*0.07)
    image_full.paste(image_text,(0,0))
    image_full.paste(image_barcode,(int(SIZE[0]*0.2),Y_INDEND))
    image_full.save(f"datamatrix_data.jpg") 
    change_printer_status(1,port)
    os.system(f"lp -d {name} datamatrix_data.jpg")
    os.remove(f"datamatrix_data.jpg")
    os.remove(f"barcode.jpg")
    time.sleep(2)
    change_printer_status(0,port)

def table_print(columns:list,text:list,name:str,port:str,font_size:int=100): 
    columns_count=len(columns)
    rows_count=len(text)
    font=ImageFont.truetype("./Roboto-Black.ttf",font_size)
    table_img=Image.new("RGB",SIZE,(255, 255, 255))
    drawer=ImageDraw.Draw(table_img)
    x_point=X_INDEND
    y_point=Y_INDEND
    column_distance=(SIZE[0]-X_INDEND*2)/columns_count
    row_distance=(SIZE[1]-Y_INDEND*2)/rows_count
    for column in columns:
        drawer.text((x_point,y_point),str(column),fill="black",font=font)
        x_point+=column_distance
    y_point+=row_distance
    for row in text:
        x_point=X_INDEND
        for word in row:
            drawer.text((x_point,y_point),str(word),fill="black",font=font)
            x_point+=column_distance
        y_point+=row_distance
    table_img.save("table_img.jpg")
    change_printer_status(1,port)
    os.system(f"lp -d {name} table_img.jpg")
    os.remove(f"table_img.jpg")
    time.sleep(2)
    change_printer_status(0,port)

def text_print(text:str,name:str,port:str,font_size:int=100):
    font=ImageFont.truetype("./Roboto-Black.ttf",font_size)
    text_img=Image.new("RGB",SIZE,(255,255,255))
    drawer=ImageDraw.Draw(text_img)
    single_biggest_symbol=font.getlength("a")
    offset_box=font.getbbox("a")
    offset=(offset_box[3]-offset_box[1])*1.5
    string_legth=SIZE[0]-X_INDEND/2
    string_width=string_legth/single_biggest_symbol
    x_point=X_INDEND
    y_point=Y_INDEND
    for line in textwrap.wrap(text,string_width):
        drawer.text((x_point,y_point), line,fill="black",font=font)
        y_point+=offset
    text_img.save("text_img.jpg")
    change_printer_status(1,port)
    os.system(f"lp -d {name} text_img.jpg")
    os.remove(f"text_img.jpg")
    time.sleep(2)
    change_printer_status(0,port)

def change_printer_status(command:int,port:str):
    os.system(f"sudo ./printer_activate.sh {command} {port}")

if __name__=="__main__":
    zero=0
    #table_img_print(4,4,["","ИЮНЬ","ИЮЛЬ","Август"],[["Артем",80000,60000,70000],["Игорь",25000,20000,0],["Роман",40000,50000,70000],["Лера",45000,40000,50000]])
    #datamatrix_print("Maksimum18simvolov было,но я осилил сделать больше")
    text_print("Привет я Игорь, я не знаю что я делаю, но я делаю это стараясь и с душой","TSC_TE200_big","1-4",200)