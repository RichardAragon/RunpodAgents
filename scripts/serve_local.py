from src.config import settings
from src.server import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)
