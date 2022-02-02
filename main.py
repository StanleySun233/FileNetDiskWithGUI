import tkinter as tk
import numpy as np
import requests
from PIL import Image, ImageTk
import minio
import fun
import cv2
import threading
from tkinter.filedialog import (askopenfilename,
                                askopenfilenames,
                                askdirectory,
                                asksaveasfilename)

global maxLen, fileL, nowPage, picTable, bucket

ip = '127.0.0.1'
port = '9000'
account = "minioadmin"
password = "minioadmin"
img_size = (100, 100)

client = minio.Minio(ip + ':' + port, access_key=account, secret_key=password, secure=False)
filePack = fun.getBucketList(client)

mainWindow = tk.Tk()
mainWindow.geometry("800x600")
mainWindow.title('花鸟')
mainWindow.resizable(False, False)


def chooseDocument(event):
    global maxLen, fileL, nowPage, picTable, bucket
    docu = event.y // 20
    bucket = filePack[docu]
    fileL = fun.getObjectList(client, bucket)
    maxLen = len(fileL) // 9
    nowPage = 1
    picTable = []

    cnt = 1
    for i in fileL:
        print(i)
        threading.Thread(picTable.append(fun.fileDownload_PIC(client, bucket, i)))
        cnt +=1
    showPage.configure(text='第{}页，共{}页'.format(nowPage, maxLen + 1))
    clearPage()
    changeBeginPic()


def clearPage():
    for i in picLabel:
        i.configure(bg='lightblue', image=ImageTk.PhotoImage(Image.open('empty.png')))


def changeBeginPic():
    l = [9, len(picTable)][len(picTable) <= 9]
    for i in range(l):
        picLabel[i].configure(image=picTable[i])


def changeRightPage(*args):
    global nowPage
    if nowPage < maxLen + 1:
        clearPage()
        showPage.configure(text='第{}页，共{}页'.format(nowPage + 1, maxLen + 1))
        index = 0
        for i in range(nowPage * 9, min((nowPage + 1) * 9, len(picTable))):
            picLabel[index].configure(image=picTable[i])
            index += 1
        nowPage += 1


def changeLeftPage(*args):
    global nowPage
    if nowPage > 1:
        clearPage()
        showPage.configure(text='第{}页，共{}页'.format(nowPage - 1, maxLen + 1))
        index = 0
        for i in range((nowPage - 2) * 9, (nowPage - 1) * 9):
            picLabel[index].configure(image=picTable[i])
            index += 1
        nowPage -= 1
        print(picLabel[0].config('text')[-1])


def downloadPic(event):
    index = int(event.widget['text'])
    filename = fileL[(nowPage - 1) * 9 + index]
    print(filename)
    path = asksaveasfilename(title='选择文件夹', initialfile=filename)
    print(path)
    url = fun.fileDownload(client, bucket, filename)
    url = requests.get(url)
    data = open(path, 'wb')
    data.writelines(url)
    data.close()


def uploadPic():
    path = askopenfilenames()
    for i in path:
        name = i[len(i) - (i[::-1]).index('/'):]
        url = fun.fileUploadURL(client, bucket, path=i)


FileList = tk.Listbox(mainWindow)
for i in filePack[::-1]:
    FileList.insert(0, i)
FileList.pack(side='left')
FileList.place(x=50, y=100, width=100, height=360)
FileList.bind('<Button-1>', func=chooseDocument)

Label1 = tk.Label(mainWindow, text='文件夹', bg="LightBlue")
Label1.place(x=50, y=0, width=100, height=40)

Label2 = tk.Label(mainWindow, text='文件', bg='lightBlue')
Label2.place(x=320, y=0, width=100, height=40)

x_beg = 200
y_beg = 100
picLabel = []
pictureTable = tk.Label(mainWindow, bg='gray')
pictureTable.pack()
pictureTable.place(x=190, y=90, width=360, height=360)

for i in range(3):
    for j in range(3):
        res = i * 3 + j
        label_img = tk.Button(pictureTable, text=str(i * 3 + j), bg='blue', name=str(i * 3 + j))
        label_img.bind('<Button-1>', func=downloadPic)
        label_img.pack()
        picLabel.append(label_img)
        picLabel[3 * i + j].pack(side='bottom')
        picLabel[3 * i + j].place(x=8 + i * 120, y=8 + j * 120, width=100, height=100)

left_but = tk.Button(mainWindow, text="上一页", command=changeLeftPage)
left_but.pack(side='bottom')
left_but.place(x=260, y=460, width=100, height=30)

right_but = tk.Button(mainWindow, text="下一页", command=changeRightPage)
right_but.pack(side='bottom')
right_but.place(x=380, y=460, width=100, height=30)

upload_but = tk.Button(mainWindow, text="上传图片", command=uploadPic)
upload_but.pack(side='bottom')
upload_but.place(x=320, y=550, width=100, height=30)

showPage = tk.Label(mainWindow)
showPage.pack()
showPage.place(x=320, y=500, width=150, height=30)

mainWindow.mainloop()
