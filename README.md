# DaDaStock

## 模擬股票網站

![image](https://user-images.githubusercontent.com/47053728/156542264-00cd092e-2328-4ad2-b0dc-7df746b17fae.png)


<p>模擬一般的股票網站，可以下單、查看個人資訊、查看股票資訊</p>

<p>採用前後端分離，後端為Python - Django，前端為Vue</p>

### RUN backend

<p>先使用python manage.py migrate 產生資料庫</p>

<p>接下來可使用python manage.py runserver</p>

<p>或者使用uwsgi --ini uwsgi.ini</p>


### RUN frontend

<p>進入frontend的stockapp資料夾</p>

<p>使用npm install 安裝鎖需模組</p>

<p>接著回到package.json所在目錄層</p>

<p>使用npm run serve運行</p>

<a href="http://34.67.216.186:8097/stockapp/#">點我前往範例</a>

