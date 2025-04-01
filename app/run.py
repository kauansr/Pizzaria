from src.main.server.server import create_app
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=3000, debug=os.getenv("DEBUG"))
