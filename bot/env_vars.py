import dotenv
import os

dotenv.load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
FLASK_API = os.getenv('FLASK_API')
USE_WEBHOOK = os.getenv("USE_WEBHOOK", 0)
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # For webhook mode
WEBAPP_HOST = os.getenv("WEBAPP_HOST", "0.0.0.0")
WEBAPP_PORT = int(os.getenv("WEBAPP_PORT", 5050))
