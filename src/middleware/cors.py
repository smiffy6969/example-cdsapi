from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.template import Template

def middleware(app: FastAPI, template: Template):
	app.add_middleware(
		CORSMiddleware, allow_origins=template.origins,
    	allow_credentials=True,
    	allow_methods=["*"],
    	allow_headers=["*"]
	)