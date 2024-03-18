import os
from . import app
import uvicorn


PORT = int(os.getenv("PORT", 3000))
LOG_LEVEL = os.getenv("LOG_LEVEL", "debug")

uvicorn.run(app, port=PORT, log_level=LOG_LEVEL , loop="uvloop", host="0.0.0.0")
