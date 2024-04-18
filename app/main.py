from fastapi import FastAPI, WebSocket, Depends
from fastapi.responses import HTMLResponse
import logging
from logging.handlers import RotatingFileHandler
import asyncio

app = FastAPI()

# Setup advanced logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[RotatingFileHandler("app_logs.log", maxBytes=1000000, backupCount=3)])
logger = logging.getLogger(__name__)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>OCR Processing Status</title>
    </head>
    <body>
        <h1>WebSocket Test</h1>
        <button onclick='connectWebSocket()'>Connect</button>
        <script>
            function connectWebSocket() {
                var ws = new WebSocket('ws://localhost:8000/ws');
                ws.onmessage = function(event) {
                    var message = event.data;
                    document.body.append(message + '<br>');
                };
                ws.onerror = function(event) {
                    console.error('WebSocket error observed:', event);
                };
                ws.onclose = function(event) {
                    console.log('WebSocket connection closed', event);
                };
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        for i in range(100):
            await websocket.send_text(f'Message {i}')
            await asyncio.sleep(1)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()

        await websocket.send_text(f'Message {i}')
            await asyncio.sleep(1)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        for i in range(100):
            await websocket.send_text(f'Message {i}')
            await asyncio.sleep(1)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()

