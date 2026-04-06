from typing import List, Dict
from fastapi import FastAPI
from pydantic import BaseModel
from app.api.routes.routers import router

app = FastAPI() 

app.include_router(router)

def main():
    print("Hello from buddysplit!")


if __name__ == "__main__":
    main()
