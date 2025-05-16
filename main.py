from fastapi import FastAPI

from src.template import load
from src.router import router
from src.middleware.cors import middleware as cors_middleware

template = load()

app = FastAPI()

# inner most middleware
cors_middleware(app, template)

router(app, template.routes)
