from fastapi import FastAPI
from src.router import customer_routes

app = FastAPI()


app.include_router(customer_routes.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Customer Management API"}
