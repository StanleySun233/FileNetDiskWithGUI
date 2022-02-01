import os
import time
import tkinter as tk
from PIL import Image, ImageTk
import minio
import cv2
import requests


def fileDownload_PIC(client: minio.Minio, bucket: str, name: str) -> [bool, str]:
    if isBucketExist(client, bucket):
        url = client.presigned_get_object(bucket, name)
        data = requests.get(url)
        f = open(name, 'wb')
        f.writelines(data)
        f.close()
        return pic2tkpic(name, (100, 100))
    else:
        return False


def fileDownload(client: minio.Minio, bucket: str, name: str) -> [bool, str]:
    if isBucketExist(client, bucket):
        url = client.presigned_get_object(bucket, name)
        return url
    else:
        return False


def fileUploadURL(client: minio.Minio, bucket: str, path: str, name: str = None) -> bool:
    try:
        if not name:
            name = path[len(path) - (path[::-1]).index('/'):]
            name = str(int(time.time()*1000)) + name[name.index("."):]
            print(name)
        file = open(path, 'rb')
        url = client.presigned_put_object(bucket, name)
        requests.put(url, file)
        return True
    except Exception:
        return False


def isObjectExist(client: minio.Minio, bucket: str, name: str) -> bool:
    try:
        flag = isBucketExist(client, bucket)
        if flag:
            url = fileDownload_PIC(client, bucket, name)
            return True
        else:
            return False
    except Exception:
        return False


def isBucketExist(client: minio.Minio, bucket: str) -> bool:
    try:
        flag = client.bucket_exists(bucket)
        return flag
    except Exception:
        return False


def makeBucket(client: minio.Minio, bucket: str) -> bool:
    try:
        client.make_bucket(bucket)
        return True
    except Exception:
        return False


def getBucketList(client: minio.Minio) -> [bool, list]:
    try:
        res = client.list_buckets()
        list = []
        for i in res:
            list.append(str(i))
        return list
    except Exception:
        return False


def getObjectList(client: minio.Minio, bucket: str) -> [bool, list]:
    try:
        res = client.list_objects(bucket)
        list = []
        for i in res:
            list.append(i.object_name)
        return list
    except Exception:
        return False


def pic2tkpic(img, img_size):
    img_ = cv2.imread(img)
    os.remove(img)
    img__ = cv2.resize(img_, img_size)
    img__ = cv2.cvtColor(img__, cv2.COLOR_BGR2RGB)
    img___ = Image.fromarray(img__)
    img____ = ImageTk.PhotoImage(image=img___)
    return img____
