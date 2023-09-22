from fastapi import FastAPI
from starlette.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def main_page():
    return """
    <html>
    <body>
    <a href="https://freekassa.ru" target="_blank" rel="noopener noreferrer">
  <img src="https://cdn.freekassa.ru/banners/big-dark-1.png" title="Прием платежей на сайте">
</a></body></html>
    """
