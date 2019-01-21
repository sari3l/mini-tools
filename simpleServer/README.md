# 简易服务器

因`ceye.io`不记录 https 请求，特此记录下

## 方法 1

burp - Collaborator client 支持 http & https

## 方法 2

### HTTP

```python
# py2
python -m SimpleHTTPServer <port>

# py3
python -m http.server <port>
```

### HTTPS

1. 执行命令生成 PEM 文件

    ```bash
    openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
    ```

2. 执行对应版本`simple-https-server.py`，脚本里只简单记录`GET PATH`，可自行修改或使用`https-server.py`获取`header`


