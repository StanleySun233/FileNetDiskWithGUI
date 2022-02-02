# 花鸟画元素分类存储

## 一. MinIO for WIndows 10

### 1. 下载

```
https://dl.minio.io/server/minio/release/windows-amd64/minio.exe
```

### 2. 启动服务

保存下载的地方，例如 `E:\ship\MinIO` 。
在下载的文件夹按下 `Shift` + `右键` ，打开 `Windows Power Shell` ，输入： 

```
.\minio.exe server E:\ship\MinIO --console-address ":9090"
```

#### 3. 记录信息

显示如下信息即为成功启动MinIO服务。

```
API: http://192.168.2.188:9000  http://127.0.0.1:9000
RootUser: minioadmin
RootPass: minioadmin

Console: http://192.168.2.188:9090 http://127.0.0.1:9090
RootUser: minioadmin
RootPass: minioadmin
```

地址为： `http://192.168.2.188:9000` 。

本地访问可以改成： `http://127.0.0.1:9000` 。

账号为： `minioadmin` 。

密码为： `minioadmin` 。

端口为： `9000` 和 `9090` 。

## 二. Python

### 1. Anaconda

根据版本自行下载。

```
https://www.anaconda.com/products/individual
```

### 2. 需求库

本项目使用 `Python 3.7` 。

```
pip install opencv-python
pip install minio
pip install pillow
```